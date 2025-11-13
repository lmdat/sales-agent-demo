<template>
    <div class="flex w-full h-10 border-b border-gray-200 items-center justify-between">
        <div>
            <Button 
                label="New Conversation"
                :severity="disabledNewConversation ? 'secondary' : 'warn'"
                variant="text"
                size="small"
                icon="pi pi-bolt"
                :disabled="disabledNewConversation"
                @click="newConversationBtnClick"/>
            <!-- <ConfirmDialog></ConfirmDialog> -->
        </div>
    </div>
</template>

<script setup>
import Button from 'primevue/button';
import { useChatStore } from '../stores/chat';
import { nextTick } from 'vue';

const chatStore = useChatStore();

const newConversationBtnClick = () => {
    console.log('New Conversation Button Clicked');
    chatStore.newThread(); 
    chatStore.getHistoryMessages().then(() => scrollToBottom());    
}

const scrollToBottom = () => {
  nextTick(() => {
    const chatContainer = document.getElementById('messages-container');
    if (chatContainer)
        chatContainer.scrollTop = chatContainer.scrollHeight;
  });
};
</script>

<style>

</style>