import { useEffect, useState } from "react"

export function JobRows(props: { ids: string[] }) {
  const [ticks, setTicks] = useState(0)
  useEffect(() => {
    const timer = setInterval(() => {
      props.ids.forEach((id) => {
        fetch("/jobs/" + id)
      })
      setTicks((n) => n + 1)
    }, 1000)
    return () => clearInterval(timer)
  }, [props.ids])
  return (
    <ul>
      {props.ids.map((id, index) => <li key={index}>{id}:{ticks}</li>)}
    </ul>
  )
}
