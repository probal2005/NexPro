# 09. for, while, break ও continue

[← আগের পাঠ](08-conditionals.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](10-strings.md)

Loop একই কাজ বারবার চালায়। for ডেটার ওপর চলে, while প্রতিবার শর্ত যাচাই করে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| for | `for item in items … end` | list-এর আইটেম, string-এর অক্ষর বা dictionary-এর key |
| while | `while condition … end` | শর্ত সত্য থাকা পর্যন্ত চালায় |
| break | `break` | নিকটতম loop শেষ করে |
| continue | `continue` | চলতি iteration-এর বাকি অংশ এড়ায় |

## কখন এবং কেন ব্যবহার করবে

খালি বা ভুল এন্ট্রি এড়িয়ে বৈধ এন্ট্রির মোট বের করো।

**সুবিধা।** একই নিয়ম অনেক রেকর্ডে ব্যবহার করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** while-এর শর্ত কখনো মিথ্যা না হলে loop শেষ হবে না। যে list-এ loop চলছে সেটিতে append করলে নতুন আইটেমও দেখা যেতে পারে।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/09-loops.pa)

```text
total = 0
for score in [4, -1, 6, 0, 9]
    if score < 0
        continue
    end
    if score == 0
        break
    end
    total = total + score
end
say total
count = 2
while count > 0
    say count
    count = count - 1
end
```

**প্রত্যাশিত ফল**

```text
10
2
1
```

## অনুশীলন

০-এর পরের ৯ কি যোগ হয়েছে?

<details>
<summary>উত্তর দেখো</summary>

হয়নি। `break` ০ দেখেই for loop শেষ করে।

</details>

[← আগের পাঠ](08-conditionals.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](10-strings.md)
