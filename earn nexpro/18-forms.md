# 18. ফর্ম ও input controls

[← আগের পাঠ](17-csv.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](19-validation.md)

ফর্মের ঘর সরাসরি .pa function দিয়ে ঘোষণা করা যায়।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Number | `number_field(label, default, min, max, step, message)` | সীমা, ধাপ ও ভুলের বার্তাসহ সংখ্যা |
| Text | `text_field(label, default)` | টেক্সট |
| Select | `select_field(label, options, default)` | একটি dropdown option |
| Checkbox | `checkbox_field(label, default)` | boolean মান |
| Result | `result(label, value)` | নামসহ আউটপুট |

## কখন এবং কেন ব্যবহার করবে

একই কোডে কোটেশনের ইনপুট ও গণনার নিয়ম রাখো। Preview tool চাপো, ঘর বদলাও, তারপর Calculate চাপো।

**সুবিধা।** নিজের HTML লেখা ছাড়াই ব্যবহারযোগ্য ফর্ম তৈরি হয়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** ফর্মের লেবেল অনন্য রাখো। CLI ও compiled Python-এ field থেকে default পাওয়া যায় এবং result stdout-এ যায়।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Preview tool** চাপো। [উদাহরণের .pa ফাইল](examples/18-forms.pa)

```text
client = text_field("Client", "Ada")
hours = number_field("Hours", 4, 1, 20, 1)
currency = select_field("Currency", ["BDT", "USD"], "BDT")
include_fee = checkbox_field("Include service fee", true)
total = hours * 50
if include_fee
    total = total + 25
end
result("Client", client)
result("Currency", currency)
result("Total", total)
```

**প্রত্যাশিত ফল**

```text
Client: Ada
Currency: BDT
Total: 225
```

## অনুশীলন

সার্ভিস ফি checkbox বন্ধ করলে কী ফল?

<details>
<summary>উত্তর দেখো</summary>

Total `200`।

</details>

[← আগের পাঠ](17-csv.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](19-validation.md)
