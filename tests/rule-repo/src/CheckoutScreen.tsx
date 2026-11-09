function PromoBanner() {
  return <p>Promo</p>
}

export function CheckoutScreen() {
  return (
    <section>
      <PromoBanner />
      <button type="submit">Pay</button>
    </section>
  )
}
