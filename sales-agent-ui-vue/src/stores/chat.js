import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";
import { ref, computed, inject } from "vue";
import axios from "axios";
import moment from 'moment';
import { v4 as uuidv4 } from 'uuid';
import * as helpers from '../utils/helpers';

export const useChatStore = defineStore("chat", () => {

    const options = inject('options');    
    const chatMessages = ref([]);
    const isBotTyping = ref(false);
    
    const selected_thread_id = useStorage(
        'selected_thread_id',
        '',
        localStorage,
        {
            mergeDefaults: true
        }
    );;

    const thread_list = useStorage(
        'thread_list',
        [],
        localStorage,
        {
            mergeDefaults: true
        }
    );

    // Computed
    const getThreadList = computed(() => {
        return [...thread_list.value].reverse();
    });


    // Actions
    const newThread = (title=null) => {
        console.log("New Thread Called")
        const _id = uuidv4()
        thread_list.value.push({
            id: _id,
            title: title ?? moment().format('YYYY-MM-DD HH:mm:ss')
        });
        selected_thread_id.value = _id
        chatMessages.value = [];
    }

    const deleteThread = async (id) => {
        console.log("Delete Thread Called", id)
        const url = `${options.serverUrl}/ai/delete-conversation`;

        const payload = {
            thread_id: id
        }

        try{
            const response = await axios.post(url, payload);
            thread_list.value = thread_list.value.filter(thread => thread.id !== id);
            selected_thread_id.value = '';
            if(thread_list.value.length > 0){
                selected_thread_id.value = thread_list.value[thread_list.value.length - 1].id
            }
            console.log("Selected thhread id after deleted ", selected_thread_id.value)
        }
        catch(err){
            console.log(err);
        }
        finally{
            chatMessages.value = [];
        }        
    }

    const selectThread = (id) => {
        console.log("Select Thread Called", id)
        selected_thread_id.value = id;
    }

    const getHistoryMessages = async () => {
        if (selected_thread_id.value == '')
            return
        console.log("Get History Messages Called", selected_thread_id.value)
        
        const url = `${options.serverUrl}/ai/history`;
        const payload = {
            thread_id: selected_thread_id.value
        }

        try{
            const response = await axios.post(url, payload);

            // console.log(response.data.history_messages)
            chatMessages.value = [];
            for(const message of response.data.history_messages){
                if (message.role == 'human' || message.role == 'user'){
                    chatMessages.value.push(helpers.createHumanMessage(message));
                }
                else{
                    chatMessages.value.push(helpers.createChatbotMessage(message));
                }                
            }
            console.log((chatMessages.value));
            
        }
        catch(err){
            console.log(err);
        }
    }

    const sendMessage = async (humanMessage) => {       
        try{
            chatMessages.value.push(helpers.createHumanMessage({"content": humanMessage}));
            isBotTyping.value = true;
            const url = `${options.serverUrl}/ai/conversation`;
            const payload = {
                thread_id: selected_thread_id.value,
                message: humanMessage
            }
            // console.log(payload)
            const response = await axios.post(url, payload);
            // console.log(response.data);
            const botMessage = response.data.message;
            chatMessages.value.push(helpers.createChatbotMessage(botMessage));
            
        }
        catch(err){
            console.log(err.response);
            console.log(err);
            console.log(err.response.data.message.content);
            const error_status = `<p>${err.response.statusText} (${err.response.status})</p>`
            chatMessages.value.push(helpers.createChatbotErrorMessage(err.response.data.message, error_status));
        }
        finally{
            isBotTyping.value = false;
        }
    }

    return{
        newThread,
        deleteThread,
        selectThread,
        getHistoryMessages,
        sendMessage,
        getThreadList,
        selected_thread_id,
        isBotTyping,
        chatMessages
    }
   
})