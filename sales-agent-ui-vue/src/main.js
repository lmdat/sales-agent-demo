import { createApp } from 'vue'
import './style.css'
import 'primeicons/primeicons.css'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import App from './App.vue'


const eleRootId = 'app';
const rootContainer = document.getElementById(eleRootId);
const _params = JSON.parse(rootContainer.dataset.params);

let options = {
    "serverUrl": import.meta.env.VITE_BASE_API_URL
}

options = Object.assign(options, _params)
console.log(options)

const pinia = createPinia()
const app = createApp(App)

app.provide('options', options)
app.use(pinia)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: false || 'none',
        }
    }
});
app.mount(`#${eleRootId}`);