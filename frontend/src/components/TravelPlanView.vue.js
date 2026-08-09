const __VLS_props = defineProps();
const money = (value) => `¥${Number(value || 0).toLocaleString('zh-CN')}`;
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
    ...{ class: "plan-card" },
});
/** @type {__VLS_StyleScopedClasses['plan-card']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "plan-heading" },
});
/** @type {__VLS_StyleScopedClasses['plan-heading']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
    ...{ class: "eyebrow" },
});
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.h2, __VLS_intrinsics.h2)({});
(__VLS_ctx.plan.destination);
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "plan-meta" },
});
/** @type {__VLS_StyleScopedClasses['plan-meta']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
(__VLS_ctx.plan.days);
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
(__VLS_ctx.money(__VLS_ctx.plan.budget));
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "day-list" },
});
/** @type {__VLS_StyleScopedClasses['day-list']} */ ;
for (const [item] of __VLS_vFor((__VLS_ctx.plan.schedule))) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.section, __VLS_intrinsics.section)({
        key: (item.day),
        ...{ class: "day-item" },
    });
    /** @type {__VLS_StyleScopedClasses['day-item']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "day-number" },
    });
    /** @type {__VLS_StyleScopedClasses['day-number']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.small, __VLS_intrinsics.small)({});
    __VLS_asFunctionalElement1(__VLS_intrinsics.strong, __VLS_intrinsics.strong)({});
    (String(item.day).padStart(2, '0'));
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "day-content" },
    });
    /** @type {__VLS_StyleScopedClasses['day-content']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.h3, __VLS_intrinsics.h3)({});
    (item.title);
    __VLS_asFunctionalElement1(__VLS_intrinsics.ul, __VLS_intrinsics.ul)({});
    for (const [activity] of __VLS_vFor((item.activities))) {
        __VLS_asFunctionalElement1(__VLS_intrinsics.li, __VLS_intrinsics.li)({
            key: (activity),
        });
        (activity);
        // @ts-ignore
        [plan, plan, plan, plan, money,];
    }
    __VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
        ...{ class: "day-notes" },
    });
    /** @type {__VLS_StyleScopedClasses['day-notes']} */ ;
    __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
    (item.transportation);
    __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({});
    (item.accommodation_suggestion);
    // @ts-ignore
    [];
}
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "plan-bottom" },
});
/** @type {__VLS_StyleScopedClasses['plan-bottom']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.section, __VLS_intrinsics.section)({});
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
    ...{ class: "eyebrow" },
});
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.div, __VLS_intrinsics.div)({
    ...{ class: "food-tags" },
});
/** @type {__VLS_StyleScopedClasses['food-tags']} */ ;
for (const [food] of __VLS_vFor((__VLS_ctx.plan.food))) {
    __VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
        key: (food),
    });
    (food);
    // @ts-ignore
    [plan,];
}
__VLS_asFunctionalElement1(__VLS_intrinsics.section, __VLS_intrinsics.section)({
    ...{ class: "budget-summary" },
});
/** @type {__VLS_StyleScopedClasses['budget-summary']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.span, __VLS_intrinsics.span)({
    ...{ class: "eyebrow" },
});
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
__VLS_asFunctionalElement1(__VLS_intrinsics.strong, __VLS_intrinsics.strong)({});
(__VLS_ctx.money(__VLS_ctx.plan.budget_breakdown.total_estimated));
__VLS_asFunctionalElement1(__VLS_intrinsics.small, __VLS_intrinsics.small)({});
(__VLS_ctx.money(__VLS_ctx.plan.budget_breakdown.transportation));
(__VLS_ctx.money(__VLS_ctx.plan.budget_breakdown.accommodation));
(__VLS_ctx.money(__VLS_ctx.plan.budget_breakdown.food));
// @ts-ignore
[plan, plan, plan, plan, money, money, money, money,];
const __VLS_export = (await import('vue')).defineComponent({
    __typeProps: {},
});
export default {};
