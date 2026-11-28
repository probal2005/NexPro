# 08. if, else ও end

[← আগের পাঠ](07-logic.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](09-loops.md)

শর্ত সত্য হলে if ব্লক চলে। মিথ্যা হলে ঐচ্ছিক else ব্লক চলে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| শুধু if | `if condition … end` | একটি শর্তসাপেক্ষ কাজ |
| if–else | `if condition … else … end` | দুটি পথের মধ্যে নির্বাচন |
| Nested if | এক ব্লকের ভিতরে আরেক `if` | একাধিক স্তরের সিদ্ধান্ত |

## কখন এবং কেন ব্যবহার করবে

পাস–ফেল বা স্টক আছে কি না দেখাও।

**সুবিধা।** ব্যবসায়িক নিয়ম কোডে সরাসরি প্রকাশ করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** প্রতিটি if-এর end দরকার। 3.6-এ আলাদা elif নেই।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/08-conditionals.pa)

```text
score = 78
if score >= 80
    say "Distinction"
else
    if score >= 50
        say "Pass"
    else
        say "Retry"
    end
end
```

**প্রত্যাশিত ফল**

```text
Pass
```

## অনুশীলন

50, 80 ও 49 দিয়ে তিনটি শাখা পরীক্ষা করো।

<details>
<summary>উত্তর দেখো</summary>

ক্রমে `Pass`, `Distinction`, `Retry`।

</details>

[← আগের পাঠ](07-logic.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](09-loops.md)
