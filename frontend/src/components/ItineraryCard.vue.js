const __VLS_props = defineProps();
const __VLS_emit = defineEmits();
const __VLS_ctx = {
    ...{},
    ...{},
    ...{},
    ...{},
};
let __VLS_components;
let __VLS_intrinsics;
let __VLS_directives;
__VLS_asFunctionalElement1(__VLS_intrinsics.article, __VLS_intrinsics.article)({
    ...{ class: "itinerary-card" },
});
/** @type {__VLS_StyleScopedClasses['itinerary-card']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "drag-handle" },
    title: "拖动调整顺序",
});
/** @type {__VLS_StyleScopedClasses['drag-handle']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "timeline-badge" },
});
/** @type {__VLS_StyleScopedClasses['timeline-badge']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.small, __VLS_intrinsics.small)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.strong, __VLS_intrinsics.strong)({});
(String(__VLS_ctx.index + 1).padStart(2, '0'));
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "itinerary-main" },
});
/** @type {__VLS_StyleScopedClasses['itinerary-main']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "itinerary-title" },
});
/** @type {__VLS_StyleScopedClasses['itinerary-title']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
(__VLS_ctx.item.dateTime);
__VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({});
(__VLS_ctx.item.location);
__VLS_asFunctionalElement1(__VLS_intrinsics.strong, __VLS_intrinsics.strong)({});
(__VLS_ctx.item.budget.toLocaleString('zh-CN'));
__VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({});
(__VLS_ctx.item.content);
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "transport" },
});
/** @type {__VLS_StyleScopedClasses['transport']} */ ;
(__VLS_ctx.item.transportation || '交通方式待补充');
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "card-actions" },
});
/** @type {__VLS_StyleScopedClasses['card-actions']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    ...{ onClick: (...[$event]) => {
            return (__VLS_ctx.$emit('edit', __VLS_ctx.item));
            // @ts-ignore
            [index, item, item, item, item, item, item, $emit,];
        } },
    type: "button",
    'aria-label': "编辑行程",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    ...{ onClick: (...[$event]) => {
            return (__VLS_ctx.$emit('remove', __VLS_ctx.item.id));
            // @ts-ignore
            [item, $emit,];
        } },
    type: "button",
    ...{ class: "danger" },
    'aria-label': "删除行程",
});
/** @type {__VLS_StyleScopedClasses['danger']} */ ;
// @ts-ignore
[];
const __VLS_export = (await import('vue')).defineComponent({
    __typeEmits: {},
    __typeProps: {},
});
export default {};
