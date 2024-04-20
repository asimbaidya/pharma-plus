# pharma-plus

## Tentative Features List for Medicine Delivery Dystem

- [x] 0.1 Flask Project structured flowing(enforcing) MVC pattern

```text
├── models // => M
│   ├── other.py
│   ├── product.py
│   └── user.py
├── templates // [View] => V
│   ├── about.html
│   ├── components
│   │   ├── flash.html
│   │   ├── layout.html
│   │   ├── nav.html
│   │   └── user-admin.html
│   ├── home.html
│   ├── login.html
│   ├── product-add.html
│   ├── product-browser.html
│   ├── product.html
│   ├── register.html
│   ├── search.html
│   └── user.html
├── controllers // [+router] => C
│   ├── pharma_plus.py
│   ├── products.py
│   ├── search.py
│   └── users.py
```

- [x] 0.2 all required model are identified and created
- [x] 0.3 dummy data generator for users and product

---

- [ ] 1. User Registration And Authentication(via email)
  - [x] 1.1 Routes for Authentication
  - [x] 1.2 View files and markup for Login forms
  - [x] 1.2 custom session data class for tracking user session
  - [ ] 1.2 form submission and backend login for Authentication
- [ ] 2. User Profile Management And Preference Setting(Information update)
- [ ] 3. Role Based Homepage(Profile Page) and User Interface(For Delivery Personnel/Admin/Users)
- [ ] 4. Medicine Inventory Management(adding medicine with image and desc.)
- [ ] 5. Insight on Medicine Storage and Notification For Low Inventory(Based on Sales Rate)

---

- [ ] 6. Browsing Search and live feedback
- [ ] 7. Ordering Medicines And Cart Management(for Over-the-counter Medicines)
- [ ] 9. Order Placing from carts and Prescribed Medicines
- [ ] 10. User's Order History Management and Overview
- [ ] 12. Scheduled Delivery Options and Subscription For Long Term Medicines
- [ ] 13. Reminder Notifications For Subscription-Based Users
- [ ] 15. Purchase Based Rewards Points and Discount System based on User's Points
- [ ] 16. Pseudo Payment Gateway Integration
- [ ] 17. Location Based anonymous Disease Tracking and Insights in the Area(Pseudo)
- [ ] 18. Delivery Movement Status and Tracking for Users
- [ ] 20. Notification System And Email With Advertisement, Awareness
- [ ] 21. Timely Reporting And Analytics Of Sells based on collected sales data to Admins
- [ ] 22. Feedback And Rating for the whole website and services
- [ ] 23. Admin Dashboard with Overall Analysis and Feedback

- [ ] 19. ^ General Advisory Or Information For Over-the-counter Medicines
- [ ] 24. Based on users Activity, Product Suggestion such as Protein Powder, Multivitamins, Supplements, et
- [ ] 14. Refund And Return Policy and Cancelation of orders, Subscriptions (based on condition)
- [ ] 11. Individual Dosage Tracking And Insights(based on order and collected info)
- [ ] 8. Prescription Upload And Medicine Availity Validation(Prescribed Medicine Ordering)

## Setup(once)

```sh
# 1. Clone repository
git clone https://github.com/asimbaidya/pharma-plus.git
```

```sh
# 2. Create virtual environment using pipenv and login to it
pipenv shell
```

```sh
# 3.  Install the dependencies
pipenv install
```

```sh
# 4. Create tables and populate with dummy data(add more dummy data)
python3 dummy-data-generator/main.py

```

```sh
# 5. Install node dependencies
npm install
```

## running(two terminal instances/tab/etc)

```sh
# 6. Run tailwind watcher
npm run tailwind
```

```sh
# 7. Run the server

python3  run.py
```
