# Earn NexPro

NexPro 3.6 শিখতে প্রথম `.pa` ফাইল থেকে শেষ CSV প্রজেক্ট পর্যন্ত ধারাবাহিক কোর্স।
প্রতিটি পাঠে সংজ্ঞা, সিনট্যাক্স, ব্যবহার, সুবিধা ও সীমাবদ্ধতা, চালানোর মতো উদাহরণ,
প্রত্যাশিত ফল এবং উত্তরসহ অনুশীলন আছে।

**কীভাবে শুরু করবে।** [NexPro Playground](https://nexpro-playground.vercel.app/)
খোলো, প্রথম পাঠের কোড পেস্ট করো এবং তার নির্দেশনা মেনে চালাও। টার্মিনালে শিখতে
[CLI ইনস্টল গাইড](../docs/HELP.md) দেখো।

| NexPro 3.6-এর অংশ | সংখ্যা | কীভাবে গোনা হয়েছে |
|---|---:|---|
| সরাসরি literal দিয়ে লেখা যায় এমন ডেটা টাইপ | ৬ | Integer, float, string, boolean, list ও dictionary |
| আলাদা expression operator | ১৩ | ৪ arithmetic চিহ্ন, ৬ comparison, ৩ logical। Unary + ও - একই চিহ্ন। |
| Statement | ১০ | অ্যাসাইনমেন্ট, say, if, while, for, break, continue, assert, return ও standalone call |
| Top-level construct | ২ | Function সংজ্ঞা ও import |
| Built-in function | ২৬ | সাধারণ ৪, string ৫, list ৭, dictionary ২, form ও CSV ৮ |
| Standard module | ৩ | Math, JSON ও CSV মিলিয়ে ৭টি function |

## ভিত্তি

1. [প্রথম .pa প্রোগ্রাম](01-first-program.md)
2. [ভেরিয়েবল ও অ্যাসাইনমেন্ট](02-variables.md)
3. [ডেটা টাইপ ও মান](03-data-types.md)
4. [ইনপুট, আউটপুট ও রূপান্তর](04-input-output.md)

## অপারেটর ও নিয়ন্ত্রণ

5. [Integer, float ও arithmetic](05-arithmetic.md)
6. [Comparison operators](06-comparisons.md)
7. [Boolean ও logical operators](07-logic.md)
8. [if, else ও end](08-conditionals.md)
9. [for, while, break ও continue](09-loops.md)

## ডেটা স্ট্রাকচার ও ফাংশন

10. [String, index, slice ও text functions](10-strings.md)
11. [List, array-এর সাধারণ কাজ ও slice](11-lists.md)
12. [Dictionary ও nested records](12-dictionaries.md)
13. [User-defined function, parameter ও scope](13-functions.md)

## মডিউল ও স্ট্যান্ডার্ড লাইব্রেরি

14. [Import ও module namespace](14-imports.md)
15. [std/math — পরম মান, rounding ও বর্গমূল](15-math.md)
16. [std/json — JSON পড়া ও লেখা](16-json.md)
17. [std/csv — টেবিল পড়া ও লেখা](17-csv.md)

## বাস্তব টুল ও প্রজেক্ট

18. [ফর্ম ও input controls](18-forms.md)
19. [Validation, assertion ও runtime error](19-validation.md)
20. [CSV upload ও নামসহ download](20-csv-tools.md)
21. [Playground, শেয়ার লিংক ও প্রকাশ](21-sharing.md)
22. [CLI, টেস্ট ও ডিবাগিং](22-cli-debug-test.md)
23. [শেষ প্রজেক্ট — স্টক থেকে পুনঃঅর্ডার](23-capstone.md)

## অতিরিক্ত রেফারেন্স

- [ভাষার রেফারেন্স](../docs/language.md) ও [ব্যাকরণ](../docs/grammar.md)
- [বাস্তব প্রজেক্ট](../projects/README.md) ও [লাইভ ডেমো](https://nexpro-playground.vercel.app/#live-projects)
