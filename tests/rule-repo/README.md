# rule-repo

Fixture. Not a product. Bad files are specimens. Do not delete them to make a review green.

```bash
python3 -m unittest tests.test_rule_repo
```

| File | What it breaks | Hook |
|---|---|---|
| `src/Checkout.tsx` | nothing | exit 0 |
| `src/BadBanner.tsx` | `console.log` | exit 2, `rules.sh` |
| `src/SecretForm.tsx` | `sk_live_` in source and in the input | exit 2, `rules.sh` |
| `src/Conflicted.tsx` | conflict marker | exit 2, gate |
| `src/Note.tsx` | raw HTML in the DOM | exit 2, `rules.sh` |
| `src/OrderList.tsx` | empty `catch`, server rows copied into `useState`, name `data` | exit 2, `rules.sh` |
| `src/JobRows.tsx` | `key={index}`, one fetch per row, no written poll rate | exit 2, `rules.sh` |
| `src/price.ts` and `src/cartPrice.ts` | same `applyDiscount` statements twice | exit 0 |
| `src/AddressForm.tsx` | five `Input` calls, only the data changes | exit 0 |
| `src/CheckoutScreen.tsx` | promo banner always on, no flag | exit 0 |
| `src/NumberField.tsx` | `isNumber` next to `type` | exit 0 |
| `src/orderStatus.ts` | client map of server status labels | exit 0 |
| `src/shared/format.ts` | shared file imports a screen | exit 0 |
| `src/saveCard.ts` | `fetch` with no await | exit 0 |
