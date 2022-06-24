# Database Matching System
![img](./Images/cropped-Stanford_Pride-S@2x.png)

Authors: 

- Saad Saeed [Github](https://github.com/ssaeed85) | [LinkedIn](https://www.linkedin.com/in/saadsaeed85/)
- Zach Rauch [Github](https://github.com/ZachRauch) | [LinkedIn](https://www.linkedin.com/in/zach-rauch/)
- Hanis Zulmuthi [Github](https://github.com/hanis-z) | [LinkedIn](https://www.linkedin.com/in/hanis-zulmuthi/)

- Xiaohua Su [Github](https://github.com/xiaohua-su) | [LinkedIn](https://www.linkedin.com/in/xiaohua-su/)
# Overview

Nonprofit organizations want to be able to bring new members and retain them.
It is vital for organizations to keep in touch with its members by communicating
to their members about events or news. Without these methods of communication, members are 
no longer in touch with the organization, and its activities. Member retention is vital for an organization and for
interacting with others. For instance, a common issue that some organizations may have is that
the email provided to the organization may no longer work or gets bounced once the individual graduates
from said institution such as colleges, and or bootcamp and updating the contact is critical to keep
them in the network. Overtime, this issue will become larger and larger for the organization, where it may
have lost touch with a vast number of its members.

The purpose of this project is to help Stanford Pride address such an issue. Stanford Pride currently
has ~5000 members in their database. Unfortunately, Stanford Pride has lost contact with a small portion of
its member. One way Stanford Pride recognizes that it has lost contact with a member that has not chosen to opt-out
of newsletter is that the newsletters was bounced. According to Stanford Pride, their members are not all using the same
platform. Some chose to have subscribed to either only emails, other are only on their Facebook, LinkedIn group and 
some use multiple platforms. As such, Stanford Pride hopes to be able to rectify the issue of lost members by 
updating the indvidual's contact information in order to bring/keep them in the network once again.

Our goal for this project is to help Stanford Pride be able to update these information in a more efficient way. We
improved the effiency by using a cosine similar model to provide a list of individuals from the Stanford Pride
database with the individual from their Mailchimp database. This way, the chair in-charge of updating their database
does not need to look up multiple potential people on their Stanford Database before deciding if they were the same individual.

From Stanford Pride:
> A nonprofit organization, such as Stanford Pride, strives by attracting and retaining members. 
> It is vital for the organization to stay in touch with its members. 
> The main means to achieve this is the sending of newsletters via e-mail. 
> Members are not likely to keep informed of the organization’s activity on their own. We only stay in their minds by regularly pushing news out to them.
Members do not always subscribe to other sources of information about the organization’s activities. 
> For example, Stanford Pride has approximately 4,400 members in its database, out of which about 3,700 currently have valid e-mail addresses. 
> Only 1,600 are part of our Facebook group, and 400 in our LinkedIn group. 
> Therefore, our monthly e-mail newsletter is our sole means to reach about 2,100 members – almost half of our total membership.


# Methodology
In order to be able to tackle this issue, we received a database of their mailchimp and Stanford Pride.
Due to the sensitive information in the data, we only received a csv file and an excel file that contained
the raw data's column names. From there, a fake dataset was created for them. In the datasets,
included some common issues mentioned as well as add some potential issues that we believe may appear down the line.

Using the fake datasets, we used cosine similarity to create a list of individuals that matched on the first name. By using,
cosine, we receive a score of similar that record is to the MailChimp record that we can then sort the list on. All the matches
on first name will still appear but the list is sorted.

# Results

# Next Step
- Integrate our model and the UI/UX designers vision for the website/app together.
- Proactive approach of asking the individuals to update their email before they graduate.
- Find someone that's willing to webscrape LinkedIn and Facebook information 