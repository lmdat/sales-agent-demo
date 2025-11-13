<template>
    <div class="mx-auto">
        <div class="flex flex-col min h-screen">
            <div class="flex flex-grow overflow-hidden">
                <aside class="flex flex-col w-1/6 h-screen">
                    <div class="flex w-full h-10 border-b border-gray-200 items-center ml-1 text-indigo-700 font-bold">
                        <img :src="sales_avatar" alt="sales_avatar" class="w-8 h-8 rounded-full">
                        <span class="ml-2">Sales Agent Assistant</span>
                    </div>
                    <div class="flex-1 px-2 overflow-y-auto pb-[20px] h-screen">
                        <div
                            v-for="thread in chatStore.getThreadList"
                            :key="thread.id"
                            class="flex items-center justify-between my-1 p-2 hover:bg-indigo-50 cursor-pointer"
                            :class="chatStore.selected_thread_id == thread.id ? 'bg-indigo-50 font-bold' : ''"
                            
                        >
                            <div 
                                @click="selectThreadClick(thread.id)"
                                class="mr-2 w-full truncate"
                            >
                                <span>{{ thread.title }}</span>
                            </div>

                            <div 
                                @click="deleteThreadClick(thread.id)"
                                class="cursor-pointer text-red-600">
                                <i class="pi pi-trash" title="Delete"></i>
                            </div>
                        </div>
                    </div> 
                </aside>

                <main class="flex w-5/6 flex-col border-l border-gray-200">
                    <!-- Header -->
                    <Header></Header>

                    <div id="messages-container" class="flex-1 h-screen overflow-y-auto p-4 space-y-4">
                        <div 
                            v-for="message in chatStore.chatMessages"
                            :key="message.id"
                            class="flex"
                            :class="message.role == 'human' ? 'justify-end' : 'justify-start'"
                        >
                            <div 
                                class="max-w-xs px-4 py-2 rounded-lg md:max-w-4xl "
                                :class="message.role == 'human' ? 'bg-teal-600 text-white' : 'bg-stone-200'">
                                <div 
                                    v-if="message.is_error" 
                                    v-html="message.error_status" 
                                    class="text-red-500 italic mt-1"></div>
                                <div 
                                    v-html="message.content"
                                    :class="message.is_error ? 'text-red-500 italic mt-1' : ''"></div>
                                <div
                                    v-if="message.role == 'ai'" 
                                    class="flex w-full items-center justify-between mt-3">
                                    <div class="text-xs text-left text-fuchsia-600 italic">
                                        Usage Tokens: Input={{ message.tokens.input ?? 0 }} | Output={{ message.tokens.output ?? 0 }} | Total={{ message.tokens.total ?? 0 }}
                                    </div>
                                    <div class="text-xs text-right italic">{{ message.time }}</div>
                                </div>
                                <div v-else class="text-xs text-right italic mt-3">{{ message.time }}</div>
                            </div>
                        </div>
                        <div v-if="chatStore.isBotTyping" class="flex justify-start">
                            <div class="flex space-x-1 max-w-xs px-4 py-2 rounded-lg md:max-w-3xl bg-stone-200 animate-pulse">
                                <div class='h-1 w-1 bg-black rounded-full animate-bounce [animation-delay:200ms]'></div>
                                <div class='h-1 w-1 bg-black rounded-full animate-bounce [animation-delay:300ms]'></div>
                                <div class='h-1 w-1 bg-black rounded-full animate-bounce [animation-delay:500ms]'></div>                                
                            </div>
                        </div>                        
                    </div>
                                        
                    <!-- Input -->
                    <div class="flex flex-col px-4 pt-4 bg-gray-100">
                        <div class="flex">
                            
                            <Textarea
                                id="input-message"
                                rows="1"
                                variant="filled"
                                class="w-full"
                                placeholder="Text me something... (Press Ctrl + Enter to send)"
                                v-model="inputMessage"
                                :disabled="disabledInput"
                                @input="adjustTextareaHeight"
                                @keydown.ctrl.enter="sendMessage"/>
                            <Button 
                                label="Send"
                                icon="pi pi-send"
                                class="ml-1"
                                :disabled="disabledBtnSend"                                
                                raised
                                @click="sendMessage"/>
                        </div> 
                        <div class="text-sm w-full py-1 text-center italic">
                            Assistant can make mistakes. Consider to check important info before use.
                        </div>
                    </div>
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import sales_avatar from '../assets/sales.jpg'
import Header from './Header.vue';
import Button from 'primevue/button';
import Textarea from 'primevue/textarea'; 
import { onMounted, onUpdated, computed, ref, nextTick } from 'vue';
import { useChatStore } from '../stores/chat';

const chatStore = useChatStore();
const inputMessage = ref('');

const usageTokens = ref({});


onMounted(() => {
    chatStore.getHistoryMessages().then(() => scrollToBottom());
    const refInputMessage = document.getElementById('input-message');
    refInputMessage.focus();    
})

onUpdated(() => {
    scrollToBottom();
    const refInputMessage = document.getElementById('input-message');
    refInputMessage.focus(); 
});

const disabledInput = computed(() => {
    return (chatStore.isBotTyping.valueOf() == true || chatStore.selected_thread_id == '');
})

const disabledBtnSend = computed(() => {
    return (chatStore.isBotTyping.valueOf() == true || inputMessage.value == '' ||chatStore.selected_thread_id == '');
})

const scrollToBottom = () => {
  nextTick(() => {
    const chatContainer = document.getElementById('messages-container');
    if (chatContainer)
        chatContainer.scrollTop = chatContainer.scrollHeight;
  });
};

const selectThreadClick = (thread_id) => {
    chatStore.selectThread(thread_id);
    chatStore.getHistoryMessages().then(() => scrollToBottom());
}

const deleteThreadClick = async (thread_id) => {
    await chatStore.deleteThread(thread_id);
    chatStore.getHistoryMessages().then(() => scrollToBottom());
}

const sendMessage = () => {
    if (inputMessage.value == '')
        return;

    chatStore.sendMessage(inputMessage.value);
    inputMessage.value = '';
    adjustTextareaHeight()
} 

const adjustTextareaHeight = () => {
    const textarea = document.getElementById('input-message');
    textarea.style.height = 'auto';
    if(textarea.scrollHeight > 100){
        textarea.style.height = '100px'
    }
    else{
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    if (inputMessage.value == ''){
        textarea.rows = 1; // Reset to one row if empty
        textarea.style.height = 'auto'; // Reset the height again
    }
}
</script>

<style>
#messages-container table{
    width: 100%;
    margin-top: 5px;
    margin-bottom: 5px;
    font-size: small;
}

#messages-container table th{
    border: 1px solid #000;
    text-align: center;
    padding: 2px;
}

#messages-container table td{
    border: 1px solid #000;
    padding: 2px;
    text-align: right;
}

#messages-container ul{
    margin-top: 5px;
    margin-bottom: 5px;    
    list-style: disc;
    margin-left: 30px;
}
</style>