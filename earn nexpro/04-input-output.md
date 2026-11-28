# 04. ইনপুট, আউটপুট ও রূপান্তর

[← আগের পাঠ](03-data-types.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](05-arithmetic.md)

input এক লাইন string হিসেবে পড়ে। সংখ্যার হিসাবের আগে প্রয়োজনে ধরন বদলাও।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| পড়া | `input()` বা `input("Name: ")` | এক লাইন পড়ে, প্রয়োজনে prompt দেখায় |
| লেখা | `say value` | ফল দেখায় |
| পূর্ণসংখ্যা | `int("12")` | string বা সংখ্যা থেকে integer |
| দশমিক | `float("1.5")` | string বা সংখ্যা থেকে float |
| দৈর্ঘ্য | `len(value)` | অক্ষর, আইটেম বা entry গোনে |

## কখন এবং কেন ব্যবহার করবে

কমান্ড লাইনের ক্যালকুলেটর বা Playground-এর Program input ব্যবহার করো। Program input-এ 4 এবং 2.5 আলাদা লাইনে দাও।

**সুবিধা।** একই কোড ভিন্ন ইনপুটে পুনরায় চালানো যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** ভুল সংখ্যা বা প্রয়োজনের চেয়ে কম ইনপুট লাইনে runtime error হবে।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/04-input-output.pa)

**Program input**-এ নিচের দুই লাইন দাও।

```text
4
2.5
```

```text
quantity = int(input())
price = float(input())
say quantity * price
```

**প্রত্যাশিত ফল**

```text
10.0
```

## অনুশীলন

প্রথম ইনপুট ৮ হলে ফল কী?

<details>
<summary>উত্তর দেখো</summary>

`20.0`।

</details>

[← আগের পাঠ](03-data-types.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](05-arithmetic.md)
