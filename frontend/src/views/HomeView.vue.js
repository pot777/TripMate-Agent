import { nextTick, ref } from 'vue';
import { useTripStore } from '../stores/trip';
import ChatSidebar from '../components/ChatSidebar.vue';
import ChatMessage from '../components/ChatMessage.vue';
const store = useTripStore();
const input = ref('');
const chatEnd = ref(null);
const suggestions = ['成都 3 天游，预算 3000 元', '周末去上海看展和吃美食', '北京亲子游，行程轻松一点'];
async function submit(text = input.value) {
    if (!text.trim())
        return;
    input.value = '';
    await store.submitMessage(text);
    await nextTick();
    chatEnd.value?.scrollIntoView({ behavior: 'smooth' });
}
const __VLS_ctx = {
    ...{},
    ...{},
};
let __VLS_components;
let __VLS_intrinsics;
let __VLS_directives;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "home-layout" },
});
/** @type {__VLS_StyleScopedClasses['home-layout']} */ ;
const __VLS_0 = ChatSidebar;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent1(__VLS_0, new __VLS_0({}));
const __VLS_2 = __VLS_1({}, ...__VLS_functionalComponentArgsRest(__VLS_1));
__VLS_asFunctionalElement1(__VLS_intrinsics.section, __VLS_intrinsics.section)({
    ...{ class: "chat-workspace" },
});
/** @type {__VLS_StyleScopedClasses['chat-workspace']} */ ;
if (!__VLS_ctx.store.messages.length) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "welcome" },
    });
    /** @type {__VLS_StyleScopedClasses['welcome']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
        ...{ class: "welcome-kicker" },
    });
    /** @type {__VLS_StyleScopedClasses['welcome-kicker']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.h1, __VLS_intrinsics.h1)({});
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({});
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "suggestions" },
    });
    /** @type {__VLS_StyleScopedClasses['suggestions']} */ ;
    for (const [suggestion] of __VLS_vFor((__VLS_ctx.suggestions))) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
            ...{ onClick: (...[$event]) => {
                    if (!(!__VLS_ctx.store.messages.length))
                        throw 0;
                    return (__VLS_ctx.submit(suggestion));
                    // @ts-ignore
                    [store, suggestions, submit,];
                } },
            key: (suggestion),
            type: "button",
        });
        (suggestion);
        // @ts-ignore
        [];
    }
}
else {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "conversation" },
    });
    /** @type {__VLS_StyleScopedClasses['conversation']} */ ;
    for (const [message] of __VLS_vFor((__VLS_ctx.store.messages))) {
        const __VLS_5 = ChatMessage;
        // @ts-ignore
        const __VLS_6 = __VLS_asFunctionalComponent1(__VLS_5, new __VLS_5({
            key: (message.id),
            message: (message),
        }));
        const __VLS_7 = __VLS_6({
            key: (message.id),
            message: (message),
        }, ...__VLS_functionalComponentArgsRest(__VLS_6));
        // @ts-ignore
        [store,];
    }
    if (__VLS_ctx.store.loading) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "message-row assistant" },
        });
        /** @type {__VLS_StyleScopedClasses['message-row']} */ ;
        /** @type {__VLS_StyleScopedClasses['assistant']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "assistant-avatar" },
        });
        /** @type {__VLS_StyleScopedClasses['assistant-avatar']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
            ...{ class: "thinking" },
        });
        /** @type {__VLS_StyleScopedClasses['thinking']} */ ;
        __VLS_asFunctionalElement1(__VLS_intrinsics.i)({});
        __VLS_asFunctionalElement1(__VLS_intrinsics.i)({});
        __VLS_asFunctionalElement1(__VLS_intrinsics.i)({});
        __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
    }
    __VLS_asFunctionalElement1(__VLS_intrinsics.div)({
        ref: "chatEnd",
    });
}
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "composer-wrap" },
});
/** @type {__VLS_StyleScopedClasses['composer-wrap']} */ ;
if (__VLS_ctx.store.error) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({
        ...{ class: "error-message" },
    });
    /** @type {__VLS_StyleScopedClasses['error-message']} */ ;
    (__VLS_ctx.store.error);
}
__VLS_asFunctionalElement1(__VLS_intrinsics.form, __VLS_intrinsics.form)({
    ...{ onSubmit: (...[$event]) => {
            return (__VLS_ctx.submit());
            // @ts-ignore
            [store, store, store, submit,];
        } },
    ...{ class: "composer" },
});
/** @type {__VLS_StyleScopedClasses['composer']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
    ...{ onKeydown: (...[$event]) => {
            return (__VLS_ctx.submit());
            // @ts-ignore
            [submit,];
        } },
    value: (__VLS_ctx.input),
    rows: "1",
    placeholder: "描述你的旅行需求，例如：10 月去成都玩 3 天，预算 3000 元…",
    disabled: (__VLS_ctx.store.loading),
});
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    type: "submit",
    disabled: (!__VLS_ctx.input.trim() || __VLS_ctx.store.loading),
    'aria-label': "发送旅行需求",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.small, __VLS_intrinsics.small)({});
// @ts-ignore
[store, store, input, input,];
const __VLS_export = (await import('vue')).defineComponent({});
export default {};
