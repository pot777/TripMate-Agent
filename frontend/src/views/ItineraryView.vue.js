import { computed, ref } from 'vue';
import draggable from 'vuedraggable';
import { useTripStore } from '../stores/trip';
import ItineraryCard from '../components/ItineraryCard.vue';
import ItineraryEditor from '../components/ItineraryEditor.vue';
const store = useTripStore();
const editorOpen = ref(false);
const editing = ref(null);
const totalBudget = computed(() => store.itinerary.reduce((total, item) => total + Number(item.budget || 0), 0));
function openEditor(item = null) {
    editing.value = item ? { ...item } : null;
    editorOpen.value = true;
}
function save(item) {
    if ('id' in item)
        store.updateItinerary(item);
    else
        store.addItinerary(item);
    editorOpen.value = false;
}
const __VLS_ctx = {
    ...{},
    ...{},
};
let __VLS_components;
let __VLS_intrinsics;
let __VLS_directives;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "itinerary-page page-container" },
});
/** @type {__VLS_StyleScopedClasses['itinerary-page']} */ ;
/** @type {__VLS_StyleScopedClasses['page-container']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.header, __VLS_intrinsics.header)({
    ...{ class: "page-heading" },
});
/** @type {__VLS_StyleScopedClasses['page-heading']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
    ...{ class: "welcome-kicker" },
});
/** @type {__VLS_StyleScopedClasses['welcome-kicker']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.h1, __VLS_intrinsics.h1)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
    ...{ onClick: (...[$event]) => {
            return (__VLS_ctx.openEditor());
            // @ts-ignore
            [openEditor,];
        } },
    ...{ class: "add-button" },
    type: "button",
});
/** @type {__VLS_StyleScopedClasses['add-button']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "summary-strip" },
});
/** @type {__VLS_StyleScopedClasses['summary-strip']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.small, __VLS_intrinsics.small)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.strong, __VLS_intrinsics.strong)({});
(__VLS_ctx.store.travelPlan?.destination || '尚未生成');
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.small, __VLS_intrinsics.small)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.strong, __VLS_intrinsics.strong)({});
(__VLS_ctx.store.itinerary.length);
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.small, __VLS_intrinsics.small)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.strong, __VLS_intrinsics.strong)({});
(__VLS_ctx.totalBudget.toLocaleString('zh-CN'));
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
if (!__VLS_ctx.store.itinerary.length) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "itinerary-empty" },
    });
    /** @type {__VLS_StyleScopedClasses['itinerary-empty']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
    __VLS_asFunctionalElement1(__VLS_intrinsics.h2, __VLS_intrinsics.h2)({});
    __VLS_asFunctionalElement1(__VLS_intrinsics.p, __VLS_intrinsics.p)({});
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
    let __VLS_0;
    /** @ts-ignore @type { | typeof __VLS_components.RouterLink | typeof __VLS_components.RouterLink} */
    RouterLink;
    // @ts-ignore
    const __VLS_1 = __VLS_asFunctionalComponent1(__VLS_0, new __VLS_0({
        to: "/",
        ...{ class: "secondary-link" },
    }));
    const __VLS_2 = __VLS_1({
        to: "/",
        ...{ class: "secondary-link" },
    }, ...__VLS_functionalComponentArgsRest(__VLS_1));
    /** @type {__VLS_StyleScopedClasses['secondary-link']} */ ;
    const { default: __VLS_5 } = __VLS_3.slots;
    // @ts-ignore
    [store, store, store, totalBudget,];
    var __VLS_3;
    __VLS_asFunctionalElement1(__VLS_intrinsics.button, __VLS_intrinsics.button)({
        ...{ onClick: (...[$event]) => {
                if (!(!__VLS_ctx.store.itinerary.length))
                    throw 0;
                return (__VLS_ctx.openEditor());
                // @ts-ignore
                [openEditor,];
            } },
        type: "button",
    });
}
else {
    let __VLS_6;
    /** @ts-ignore @type { | typeof __VLS_components.draggable | typeof __VLS_components.Draggable | typeof __VLS_components.draggable | typeof __VLS_components.Draggable} */
    draggable;
    // @ts-ignore
    const __VLS_7 = __VLS_asFunctionalComponent1(__VLS_6, new __VLS_6({
        modelValue: (__VLS_ctx.store.itinerary),
        ...{ class: "itinerary-list" },
        handle: ".drag-handle",
        animation: (220),
        ghostClass: "drag-ghost",
        itemKey: "id",
    }));
    const __VLS_8 = __VLS_7({
        modelValue: (__VLS_ctx.store.itinerary),
        ...{ class: "itinerary-list" },
        handle: ".drag-handle",
        animation: (220),
        ghostClass: "drag-ghost",
        itemKey: "id",
    }, ...__VLS_functionalComponentArgsRest(__VLS_7));
    /** @type {__VLS_StyleScopedClasses['itinerary-list']} */ ;
    const { default: __VLS_11 } = __VLS_9.slots;
    {
        const { item: __VLS_12 } = __VLS_9.slots;
        const [{ element, index }] = __VLS_vSlot(__VLS_12);
        const __VLS_13 = ItineraryCard;
        // @ts-ignore
        const __VLS_14 = __VLS_asFunctionalComponent1(__VLS_13, new __VLS_13({
            ...{ 'onEdit': {} },
            ...{ 'onRemove': {} },
            item: (element),
            index: (index),
        }));
        const __VLS_15 = __VLS_14({
            ...{ 'onEdit': {} },
            ...{ 'onRemove': {} },
            item: (element),
            index: (index),
        }, ...__VLS_functionalComponentArgsRest(__VLS_14));
        let __VLS_18;
        const __VLS_19 = {
            /** @type {typeof __VLS_18.edit} */
            onEdit: (__VLS_ctx.openEditor),
        };
        const __VLS_20 = {
            /** @type {typeof __VLS_18.remove} */
            onRemove: (__VLS_ctx.store.removeItinerary),
        };
        var __VLS_16;
        var __VLS_17;
        // @ts-ignore
        [openEditor, store, store,];
    }
    // @ts-ignore
    [];
    var __VLS_9;
}
if (__VLS_ctx.editorOpen) {
    const __VLS_21 = ItineraryEditor;
    // @ts-ignore
    const __VLS_22 = __VLS_asFunctionalComponent1(__VLS_21, new __VLS_21({
        ...{ 'onSave': {} },
        ...{ 'onClose': {} },
        item: (__VLS_ctx.editing),
        nextDay: (__VLS_ctx.store.itinerary.length + 1),
    }));
    const __VLS_23 = __VLS_22({
        ...{ 'onSave': {} },
        ...{ 'onClose': {} },
        item: (__VLS_ctx.editing),
        nextDay: (__VLS_ctx.store.itinerary.length + 1),
    }, ...__VLS_functionalComponentArgsRest(__VLS_22));
    let __VLS_26;
    const __VLS_27 = {
        /** @type {typeof __VLS_26.save} */
        onSave: (__VLS_ctx.save),
    };
    const __VLS_28 = {
        /** @type {typeof __VLS_26.close} */
        onClose: (...[$event]) => {
            if (!(__VLS_ctx.editorOpen))
                throw 0;
            return (__VLS_ctx.editorOpen = false);
            // @ts-ignore
            [store, editorOpen, editorOpen, editing, save,];
        },
    };
    var __VLS_24;
    var __VLS_25;
}
// @ts-ignore
[];
const __VLS_export = (await import('vue')).defineComponent({});
export default {};
