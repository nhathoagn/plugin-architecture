export function saveCard(body: string) {
  fetch("/cards", { method: "POST", body })
}
