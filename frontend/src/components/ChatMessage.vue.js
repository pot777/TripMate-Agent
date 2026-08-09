import { isTravelPlan } from '../types';
import TravelPlanView from './TravelPlanView.vue';
const __VLS_props = defineProps();
const __VLS_ctx = {
    ...{},
    ...{},
    ...{},
    ...{},
};
let __VLS_components;
let __VLS_intrinsics;
let __VLS_directives;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: (['message-row', __VLS_ctx.message.role]) },
});
/** @type {__VLS_StyleScopedClasses['message-row']} */ ;
if (__VLS_ctx.message.role === 'assistant') {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "assistant-avatar" },
    });
    /** @type {__VLS_StyleScopedClasses['assistant-avatar']} */ ;
}
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "message-body" },
});
/** @type {__VLS_StyleScopedClasses['message-body']} */ ;
if (__VLS_ctx.isTravelPlan(__VLS_ctx.message.content)) {
    const __VLS_0 = TravelPlanView;
    // @ts-ignore
    const __VLS_1 = __VLS_asFunctionalComponent1(__VLS_0, new __VLS_0({
        plan: (__VLS_ctx.message.content),
    }));
    const __VLS_2 = __VLS_1({
        plan: (__VLS_ctx.message.content),
    }, ...__VLS_functionalComponentArgsRest(__VLS_1));
}
else {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "message-bubble" },
    });
    /** @type {__VLS_StyleScopedClasses['message-bubble']} */ ;
    (typeof __VLS_ctx.message.content === 'string' ? __VLS_ctx.message.content : __VLS_ctx.message.content.message);
}
__VLS_asFunctionalElement1(__VLS_intrinsics.time, __VLS_intrinsics.time)({});
(new Date(__VLS_ctx.message.createdAt).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }));
// @ts-ignore
[message, message, message, message, message, message, message, message, isTravelPlan,];
const __VLS_export = (await import('vue')).defineComponent({
    __typeProps: {},
});
export default {};
