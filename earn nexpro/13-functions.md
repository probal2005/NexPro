# 13. User-defined function, parameter ও scope

[← আগের পাঠ](12-dictionaries.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](14-imports.md)

Function একবার সংজ্ঞায়িত করে বারবার ব্যবহার করা যায়।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| সংজ্ঞা | `function total(price, quantity) … end` | function-এর নাম ও parameter |
| Call | `total(50, 3)` | parameter-এ argument বসিয়ে চালায় |
| Return | `return price * quantity` | কলারের কাছে ফল ফেরত দেয় |
| Local scope | function-এর অভ্যন্তরের assignment | প্রতিটি call নিজের মান রাখে |
| Global lookup | ফাইলের top-level ভেরিয়েবল পড়া | local মান না পেলে global-এ খোঁজে |

## কখন এবং কেন ব্যবহার করবে

একই subtotal বা validation নিয়ম অনেক জায়গায় ব্যবহার করো।

**সুবিধা।** ব্যবসায়িক লজিক আলাদা করে পরীক্ষা করা সহজ।

**সীমাবদ্ধতা ও সাধারণ ভুল।** কলের আগে সংজ্ঞা চালাতে হবে। প্রতিটি parameter-এর একটি argument লাগে। Return ছাড়া শেষ হলে ফল None।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/13-functions.pa)

```text
tax = 5
function total(price, quantity)
    subtotal = price * quantity
    return subtotal + tax
end
say total(50, 3)
say total(25, 2)
```

**প্রত্যাশিত ফল**

```text
155
55
```

## অনুশীলন

tax = 10 করলে কী বদলাবে?

<details>
<summary>উত্তর দেখো</summary>

দুই ফলই আগের চেয়ে ৫ বাড়বে।

</details>

[← আগের পাঠ](12-dictionaries.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](14-imports.md)
