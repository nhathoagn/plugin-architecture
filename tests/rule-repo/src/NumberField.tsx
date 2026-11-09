export function NumberField(props: { isNumber: boolean, type: string }) {
  return <input type={props.isNumber ? "number" : props.type} />
}
