import { reactive, watch } from 'vue';
const props = defineProps();
const emit = defineEmits();
const form = reactive({ day: 1, dateTime: '', location: '', content: '', transportation: '', budget: 0 });
watch(() => props.item, (item) => {
    Object.assign(form, item || { day: props.nextDay, dateTime: `第 ${props.nextDay} 天`, location: '', content: '', transportation: '', budget: 0 });
}, { immediate: true });
function save() {
    if (!form.location.trim() || !form.content.trim())
        return;
    emit('save', props.item ? { ...props.item, ...form } : { ...form });
}
const __VLS_ctx = {
    ...{},
    ...{},
    ...{},
    ...{},
    ...{},
};
let __VLS_components;
let __VLS_intrinsics;
let __VLS_directives;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ onClick: (...[$event]) => {
            return (__VLS_ctx.$emit('close'));
            // @ts-ignore
            [$emit,];
        } },
    ...{ class: "modal-backdrop" },
});
/** @type {__VLS_StyleScopedClasses['modal-backdrop']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.section, __VLS_intrinsics.section)({
    ...{ class: "editor-modal" },
    role: "dialog",
    'aria-modal': "true",
    'aria-labelledby': "editor-title",
});
/** @type {__VLS_StyleScopedClasses['editor-modal']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "modal-heading" },
});
/** @type {__VLS_StyleScopedClasses['modal-heading']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
    ...{ class: "eyebrow" },
});
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.h2, __VLS_intrinsics.h2)({
    id: "editor-title",
});
(__VLS_ctx.item ? '修改行程' : '添加新行程');
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    ...{ onClick: (...[$event]) => {
            return (__VLS_ctx.$emit('close'));
            // @ts-ignore
            [$emit, item,];
        } },
    type: "button",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.form, __VLS_intrinsics.form)({
    ...{ onSubmit: (__VLS_ctx.save) },
});
__VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.input)({
    required: true,
    placeholder: "例如：第 1 天 · 上午 9:00",
});
(__VLS_ctx.form.dateTime);
__VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.input)({
    required: true,
    placeholder: "例如：成都 · 宽窄巷子",
});
(__VLS_ctx.form.location);
__VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({
    ...{ class: "full" },
});
/** @type {__VLS_StyleScopedClasses['full']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.textarea)({
    value: (__VLS_ctx.form.content),
    required: true,
    rows: "4",
    placeholder: "描述游览、用餐或休息安排",
});
__VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.input)({
    placeholder: "例如：地铁 2 号线",
});
(__VLS_ctx.form.transportation);
__VLS_asFunctionalElement1(__VLS_intrinsics.label, __VLS_intrinsics.label)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.input)({
    type: "number",
    min: "0",
    step: "1",
});
(__VLS_ctx.form.budget);
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "modal-actions full" },
});
/** @type {__VLS_StyleScopedClasses['modal-actions']} */ ;
/** @type {__VLS_StyleScopedClasses['full']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    ...{ onClick: (...[$event]) => {
            return (__VLS_ctx.$emit('close'));
            // @ts-ignore
            [$emit, save, form, form, form, form, form,];
        } },
    type: "button",
    ...{ class: "secondary" },
});
/** @type {__VLS_StyleScopedClasses['secondary']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    type: "submit",
    ...{ class: "primary" },
});
/** @type {__VLS_StyleScopedClasses['primary']} */ ;
// @ts-ignore
[];
const __VLS_export = (await import('vue')).defineComponent({
    __typeEmits: {},
    __typeProps: {},
});
export default {};
