const statusLabel: Record<string, string> = {
  "1": "Mới",
  "2": "Đang chạy",
  "3": "Xong",
}

export function labelFor(status: string) {
  return statusLabel[status] ?? "Không rõ"
}
