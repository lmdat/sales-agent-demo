import { v4 as uuidv4 } from 'uuid';
import moment from 'moment';

export const createHumanMessage = (message) => {
    // console.log('onDisplayVisitorMessage is fired');
    let _now = moment();
    if (message.time){
        _now = moment(message.time);
    }
    const _time = _now.format('DD MMM YYYY') + ' at ' + _now.format('HH:mm');
    
    return {
        id: message.id || uuidv4(),
        role: 'human',
        content: message.content,
        time: _time        
    };
};

export const createChatbotMessage = (message) => {
    let _now = moment();
    if (message.time){
        _now = moment(message.time);
    }
    const _time = _now.format('DD MMM YYYY') + ' at ' + _now.format('HH:mm');
    
    return {
        id: message.id || uuidv4(),
        role: 'ai',
        content: message.content,
        tokens: message.usage_tokens,
        is_error: false,
        time: _time,

    };
};

export const createChatbotErrorMessage = (message, error_status) => {
    let _now = moment();
    if (message.time){
        _now = moment(message.time);
    }
    const _time = _now.format('DD MMM YYYY') + ' at ' + _now.format('HH:mm');
    
    return {
        id: message.id || uuidv4(),
        role: 'ai',
        content: message.content,
        tokens: message.usage_tokens,
        is_error: true,
        error_status: error_status,
        time: _time,
    };
};