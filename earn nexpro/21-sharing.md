# 21. Playground, শেয়ার লিংক ও প্রকাশ

[← আগের পাঠ](20-csv-tools.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](22-cli-debug-test.md)

Playground থেকে কোড বা সেই কোডে তৈরি ফর্মের লিংক পাঠানো যায়।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Check syntax | Playground action | কোড parse করা যায় কি না পরীক্ষা |
| Compile to Python | Playground action | স্বতন্ত্র Python সোর্স দেখায় |
| Share code | Playground action | প্রাপকের এডিটরে source ও modules লোড হয় |
| Share tool | Playground action | প্রাপকের standalone tool page খোলে |
| View source | tool page action | সোর্স দেখা এবং Playground-এ খোলা যায় |

## কখন এবং কেন ব্যবহার করবে

নিচের সোর্স Playground-এ বসিয়ে Share tool নির্বাচন করো। লিংকটি নতুন ট্যাবে খুলে Start tool চাপো।

**সুবিধা।** ব্যবহারকারী এডিটর ছাড়াই টুল চালায়। ঝামেলা হলে সোর্সও দেখতে পারে।

**সীমাবদ্ধতা ও সাধারণ ভুল।** লিংকে কোড, মডিউল ও সোর্সে লেখা default থাকে। ফর্মে টাইপ করা তথ্য বা CSV এতে যুক্ত হয় না। Source ও module-এর JSON payload-এর সীমা 12,000 bytes।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Preview tool** চাপো। [উদাহরণের .pa ফাইল](examples/21-sharing.pa)

```text
amount = number_field("Amount", 20, 0)
result("Double", amount * 2)
```

**প্রত্যাশিত ফল**

```text
Double: 40
```

## অনুশীলন

নিজের ফর্মে Amount 30 করো। নতুন ট্যাবে মূল share link খুলে দেখো।

<details>
<summary>উত্তর দেখো</summary>

মূল লিংকে default `20`-ই দেখা যায়।

</details>

[← আগের পাঠ](20-csv-tools.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](22-cli-debug-test.md)
