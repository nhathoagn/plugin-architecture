import { useEffect, useState } from "react"

export function OrderList() {
  const [data, setData] = useState<string[]>([])
  useEffect(() => {
    async function load() {
      try {
        const response = await fetch("/orders")
        setData(await response.json())
      } catch (error) {}
    }
    load()
  }, [])
  return <ul>{data.map((row) => <li key={row}>{row}</li>)}</ul>
}
