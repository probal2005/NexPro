# 22. CLI, টেস্ট ও ডিবাগিং

[← আগের পাঠ](21-sharing.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](23-capstone.md)

Interpreter .pa সরাসরি চালায়। Compiler .pa থেকে স্বতন্ত্র Python তৈরি করে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| ইনস্টল | latest GitHub release-এর wheel + Python 3.11 বা নতুন | CLI চালানোর প্রস্তুতি |
| Run ও check | `nexpro run main.pa`, `nexpro check main.pa` | চালায় অথবা syntax ও import পরীক্ষা করে |
| Compile | `nexpro compile main.pa -o main.py` | Python তৈরি করে |
| Project | `nexpro init`, `nexpro test` | প্রজেক্ট scaffold ও প্রজেক্ট টেস্ট |
| Debug | Playground Trace execution, VS Code breakpoint/step | execution flow ও local variable দেখায় |

## কখন এবং কেন ব্যবহার করবে

টার্মিনালে নিচের উদাহরণ main.pa হিসেবে চালাও, তারপর trace-সহ Playground-এ চালিয়ে assignment ও assert-এর ক্রম দেখো।

**সুবিধা।** একই উদাহরণ CLI, Playground ও generated Python-এ পরীক্ষা করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** Syntax check কোনো ব্যবসায়িক নিয়ম ঠিক কি না যাচাই করে না। তার জন্য বিভিন্ন input ও expected output দিয়ে test লেখো।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/22-cli-debug-test.pa)

[CLI ইনস্টল গাইড](../docs/HELP.md) · [VS Code ডিবাগার](../editors/vscode/README.md)

```text
function subtotal(price, quantity)
    return price * quantity
end
assert subtotal(50, 3) == 150
say subtotal(50, 3)
```

**প্রত্যাশিত ফল**

```text
150
```

## অনুশীলন

মূল্য ৫০ থাকলেও assertion-এ expected ১৪০ লিখে চালাও।

<details>
<summary>উত্তর দেখো</summary>

Assertion ব্যর্থ হবে এবং .pa file ও line দেখাবে।

</details>

[← আগের পাঠ](21-sharing.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](23-capstone.md)
