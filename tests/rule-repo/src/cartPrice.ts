export function applyDiscount(cents: number) {
  const rate = 0.1
  const next = cents - cents * rate
  return Math.max(0, next)
}
