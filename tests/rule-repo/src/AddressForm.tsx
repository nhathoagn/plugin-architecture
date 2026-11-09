function Input(props: { label: string, name: string, autoComplete: string }) {
  return <input aria-label={props.label} name={props.name} autoComplete={props.autoComplete} />
}

export function AddressForm() {
  return (
    <form>
      <Input label="Line" name="line" autoComplete="address-line1" />
      <Input label="City" name="city" autoComplete="address-level2" />
      <Input label="Region" name="region" autoComplete="address-level1" />
      <Input label="Postal" name="postal" autoComplete="postal-code" />
      <Input label="Country" name="country" autoComplete="country" />
    </form>
  )
}
