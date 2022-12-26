<h1 align="center">Binodex</h1>

<p align="center">Registration of referrals for the <a href="https://binodex.space/">Binodex.space</a></p>
<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://img.shields.io/badge/Tor-7D4698?style=for-the-badge&logo=Tor-Browser&logoColor=white">
</p>

## ⚡ Installation
+ Install [python](https://www.google.com/search?client=opera&q=how+install+python)
+ Install [Tor Browser](https://www.torproject.org/download/)
+ [Download](https://sites.northwestern.edu/researchcomputing/resources/downloading-from-github) and unzip repository
+ Install requirements:
```python
pip install -r requirements.txt
```

## 💻 Preparing
+ Register and replenish the balance <a href="https://captcha.guru/">captcha.guru</a>
+ Launch Tor Browser
+ Run the bot:
```python
python binodex.py
```

## ✔️ Usage
+ ```Referral code``` - your referrals code
  + Example: ```https://binodex.space/?ref=0110```, code = ```0110```
+ ```Captcha key``` - key from captcha.guru(the key is on the main page)

![image](https://user-images.githubusercontent.com/119711235/209572783-62ee781d-e3ee-4f0c-a16a-6d41696421ea.png)

+ ```Delay(sec)``` - delay between referral registrations in seconds
+ ```Threads``` - number of simultaneous registrations

Temporary email addresses are used to register referrals

**Successfully registered referrals are saved in** ```registered.txt``` **in the format {email}:{password}**

## 📧 Contacts
+ Telegram - [@flamingoat](https://t.me/flamingoat)
