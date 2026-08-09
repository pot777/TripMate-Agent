export function isTravelPlan(value) {
    return typeof value === 'object' && value !== null && 'schedule' in value && 'budget_breakdown' in value;
}
