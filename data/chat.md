# Экспорт чатов WhatsApp: Kazakh Stations @ IGS
Дата экспорта: August 12, 2026 at 9:11 AM

---

## April 30, 2026

[6:44 PM] __Rui Fernandes создал(-а) группу__

[6:44 PM] __Rui Fernandes добавил(-а) участников: Вы__

[6:44 PM] __Rui Fernandes отключил(-а) исчезающие сообщения__

[6:44 PM] __Сообщения и звонки защищены сквозным шифрованием. Третьи лица, включая WhatsApp, не могут прочитать или прослушать их. Нажмите, чтобы узнать больше.__

[6:48 PM] __Нурали Назиков добавил(-а) участников: Omirzaq__

[6:57 PM] __Rui Fernandes отключил(-а) исчезающие сообщения__

---

## May 1, 2026

[4:47 PM] **Вы:** Hi @Rui Fernandes and all! I’ve put together a simple interactive map to make it easier to view all currently available sitelog information.

https://skimprem.github.io/qaz_cors_map/

We’re using the SiteLog Manager 2.0 system from IGS on our internal network (not publicly accessible) to manage the sitelog data.

[4:56 PM] **Вы:** [Документ] The source file was created by concatenating all sitelogs.

[5:00 PM] **Rui Fernandes:** Many thanks!!! It is a very good distribution!

[5:01 PM] **Rui Fernandes:** Let me turn back to you early next week….

---

## May 7, 2026

[4:54 AM] **Rui Fernandes:** I apologise the delay returning to you but I had some unexpected tasks to carry out these last days!

[4:55 AM] **Rui Fernandes:** Your network is very uniform concerning equipment, particularly the antennas. And there are also not major difference between GR50 and GR30…

[4:56 AM] **Rui Fernandes:** [Изображение]

[4:59 AM] **Rui Fernandes:** My suggestion is to divide the network into several regions - see the image, and select the best station in each region to apply for the IGS network. I considered the one in Astana because it is important to have one in the capital. I didn’t select in the southeast (near Almaty) because there are already some IGS stations nearby. But this could also be added in this regions.

[5:02 AM] **Rui Fernandes:** I would use several criteria to select the best station in each region: robustness of data communication (no data gaps), station stability (good time series), and, if of similar quality, GR50 over GR30.

[5:03 AM] **Rui Fernandes:** I’d be happy to help you submit the application further!

[5:04 AM] **Rui Fernandes:** I also would like to ask: are you processing all data and analysing the time-series to investigate the long term motion of the stations?

[6:02 AM] __Zholdasbek добавил(-а) участников: Жандос Абильдинов__

[6:48 AM] **Zholdasbek:**
> _Rui Fernandes: I apologise the delay returning to you but I had some unexpected tasks to carry out these last days!_
Hello!

[6:48 AM] **Zholdasbek:**
> _Rui Fernandes: I’d be happy to help you submit the application further!_
👍

[9:26 AM] **Нурали Назиков:**
> _Rui Fernandes: I also would like to ask: are you processing all data and analysing the time-series to investigate the long term motion of the stations?_
Hello Roi, thank you for the detailed recommendations and support.
Today are public holiday in Kazakhstan, so our team is partially unavailable. We will review everything carefully and get back to you with a more detailed response in the coming days.

[1:21 PM] **Rui Fernandes:** Happy Holiday!!! No worries… I will be waiting for your comments.

---

## May 12, 2026

[4:52 PM] **Вы:** Hello everyone.

I made an analysis of data availability (RINEX files) for each station inside the selected blocks. I also created images from these results for easier visual analysis.

I will upload these images to this chat. I also updated the interactive map by adding the block boundaries and attaching the data analysis images. To view them, you need to click on a block and then click the “View block image” link in the popup window.

Honestly, I am not very happy with our data at the moment because I can see many gaps at almost all stations during these 3 years.

However, I still hope that I have not processed all available storage locations yet, and most likely a significant part of the stations will become much more complete after that.

[4:53 PM] **Вы:** [Документ] block_1.png

[4:53 PM] **Вы:** [Документ] block_2.png

[4:53 PM] **Вы:** [Документ] block_3.png

[4:53 PM] **Вы:** [Документ] block_4.png

[4:53 PM] **Вы:** [Документ] block_5.png

[4:53 PM] **Вы:** [Документ] block_6.png

[4:53 PM] **Вы:** [Документ] block_7.png

[4:53 PM] **Вы:** [Документ] block_8.png

[4:53 PM] **Вы:** [Документ] block_9.png

[4:53 PM] __[Системное уведомление]__

[4:54 PM] **Вы:**
> _Вы: Hi @Rui Fernandes and all! I’ve put together a simple interactive map to make it easier to view all currently available sitelog information.

https://skimprem.github.io/qaz_cors_map/

We’re using the SiteLog Manager 2.0 system from IGS on our internal network (not publicly accessible) to manage the sitelog data._
The map link is here. I pinned this message

[4:58 PM] **Вы:** If you do not see the blocks on the map, please clear your browser cache and reload the page.

[4:59 PM] __Вы добавил(-а) участников: Lelyakov Anatoliy__

[8:11 PM] __Вы изменил(-а) название группы на "Kazakh Stations @ IGS"__

---

## May 13, 2026

[4:06 AM] **Rui Fernandes:** Dear @Roman Sermyagin , many thanks for the additional information... It is very useful.

[8:39 PM] **Rui Fernandes:** [Документ] I have created two tables ranking the stations at each block (but there were some other possible alternatives)

[8:41 PM] **Rui Fernandes:** Please, note that there is not only the data availability that we should have in mind. The stability of the station (that can be evaluated through the analysis of the time-series) is also very important.

[8:42 PM] **Rui Fernandes:** Are you computing the time-series for all stations?

[9:39 PM] **Вы:** Unfortunately, we haven't done this yet. I'm currently learning Bernese for series processing, but I don't think I'll be able to produce good results anytime soon. Could you suggest something we could use for a faster solution? GLab, Ginan, or maybe some other package with PPP?

---

## May 14, 2026

[2:44 AM] **Rui Fernandes:** Dear Roman and colleagues, for a quick evaluation of the stations, I suggest considering two distinct possibilities.

For a fast evaluation of the stations, I would suggest two possible options.

Option 1 — preliminary scientific assessment
From my side, as a researcher, I can help with a preliminary assessment of a few selected stations by processing them with GipsyX, which is the software I normally use for scientific GNSS time-series analysis. This could help you evaluate the stability of some candidate stations before deciding which ones are most appropriate.

Option 2 — systematic processing and analysis with MIRAseries
Please allow me to mention this separately, to avoid any misunderstanding: this is not related to my role as an IGS Governing Board member. I am involved in MIRASpaco, a company that develops GNSS-related software and services. One of its tools is MIRAseries, a software solution designed to automatically compute GNSS time series and analyse them, including the estimation of velocities, seasonal variations, offsets, and other relevant parameters.
This may be useful if you need a more systematic and operational solution for a larger number of stations. If you are interested, I can provide access to the same full-feature demo version of MIRAseries that we made available for ASC2026, so that you can test it and evaluate whether it fits your needs.

So, for the immediate need, I can help with a few stations using GipsyX. For a broader evaluation of the network, MIRAseries could be an option for you to test independently.

[6:30 AM] **Вы:** Dear Rui, thank you very much for the detailed explanation and for offering both possibilities.

We need some time to discuss these options internally with our colleagues and evaluate what would be the most appropriate approach for our network at this stage.

Your support and recommendations are highly appreciated. We will get back to you after our internal discussion.

---

## May 15, 2026

[4:11 PM] __Вы добавил(-а) участников: Самат Кинжигужинов__

[5:45 PM] **Rui Fernandes:** Of course, please take the time you need to discuss internally with your colleagues.
I would just like to stress that my assistance regarding the possible submission of some of your stations to the IGS is completely independent of any further discussion or possible collaboration concerning the options I mentioned. I will be glad to continue supporting you on the IGS-related aspects regardless of any decision on those other possibilities.

[6:30 PM] **Omirzaq:** Hello, Rui! My name is Omirzak.
Thank you for helping and supporting us with this task. Today we had a discussion regarding your proposals. We are interested in both options you suggested. We decided to review the completeness of our data and prepare a selection by stations before making a final decision.
During the discussion, your name sounded familiar to us, and then we remembered that you participated in a conference in Astana as a speaker. I am attaching the photo as well.

[6:30 PM] **Omirzaq:** [Изображение]

---

## May 16, 2026

[1:44 AM] **Rui Fernandes:**
> _Omirzaq: Hello, Rui! My name is Omirzak.
Thank you for helping and supporting us with this task. Today we had a discussion regarding your proposals. We are interested in both options you suggested. We decided to review the completeness of our data and prepare a selection by stations before making a final decision.
During the discussion, your name sounded familiar to us, and then we remembered that you participated in a conference in Astana as a speaker. I am attaching the photo as well._
Hello Omirzak… Thanks a lot for the picture! It brings me very nice memories! This station is now at ENU.

---

## May 23, 2026

[4:32 PM] **Rui Fernandes:** Good day to all of you… Independent of establishing deeper collaborations in the future, I would like to ask if you could confirm your interest in making several stations available to IGS and if you would agree that I can discuss this possibility with the other members of the Infrastructure Committee of IGS during the IGS Workshop that it is starting on next Sunday May 31th.

[5:20 PM] **Zholdasbek:** Good afternoon! Yes, we are interested and agree.

---

## May 24, 2026

[3:52 PM] **Rui Fernandes:** Would it be possible to send pictures of some of the possible stations to be suggested as IGS stations?

[3:58 PM] **Вы:** Hello, @Rui Fernandes. @Lelyakov Anatoliy has already selected several candidates from the areas you outlined. He'll post a list in this chat tomorrow. @Lelyakov Anatoliy and I have been busy filling in the data gaps for these stations for the past week. We'll need some more time to complete this work.

---

## May 25, 2026

[8:36 AM] **Lelyakov Anatoliy:** Hello @Rui Fernandes , we have carefully reviewed all the proposed areas and filtered out the unsuitable options.
Here is the final list of candidate stations selected by us, grouped by blocks:
1 Block
EIND, LORA
2 Block
RBEY, RAKT
3 Block
PZHT, DYRG
4 Block
NARS, DB0Z
5 Block
CKSH, PUZK, TNIS
6 Block
MKRJ, MSAT, MAKD
7 Block
SEKB, SSHB
8 Block
FCKР, BUSH
9 Block
ZNUR

---

## May 28, 2026

[7:08 PM] **Rui Fernandes:** Is it possible to send some pictures for some stations?

[7:11 PM] **Lelyakov Anatoliy:** Yes, we can send you photos of the stations!

[7:13 PM] **Вы:**
> _Rui Fernandes: Is it possible to send some pictures for some stations?_
Hello @Rui Fernandes ! Do you mean photos?

[7:15 PM] **Rui Fernandes:**
> _Вы: Hello @Rui Fernandes ! Do you mean photos?_
Yes! This will be required and it can help make final decision on the best stations!

[7:16 PM] **Вы:** Ok, it's possible, of course

[7:16 PM] **Rui Fernandes:**
> _Вы: Ok, it's possible, of course_
Thank you

[7:16 PM] **Lelyakov Anatoliy:** But only tomorrow🙃

[7:18 PM] **Rui Fernandes:**
> _Lelyakov Anatoliy: But only tomorrow🙃_
No worries! When you can! My plan is to discuss with my IGS colleagues during next week!

---

## May 29, 2026

[12:57 PM] **Lelyakov Anatoliy:** [Документ] for IGS.rar

---

## June 1, 2026

[7:07 AM] **Rui Fernandes:** Thank you… I am now at the IGS conference - let me check the pictures and discuss the situation with my colleagues. I will return to you asap!

---

## June 16, 2026

[3:43 PM] **Omirzaq:** Hello @Rui Fernandes  how are you? How was your IGS conference? Is there anything interesting about our question?

---

## June 17, 2026

[3:42 PM] **Rui Fernandes:** @Omirzaq , please apologise my silence, but it was very complicated days after my return - I was deeply involved in some activities of my University (it is the end of the academic year).

[3:48 PM] **Rui Fernandes:** I have spoken with my other colleagues of the Infrastructure Committee and they are really pleased to know about your commitment to have some of the stations at IGS…

[4:18 PM] **Вы:** Hello @Rui,
Thank you very much for your support and for discussing our candidate stations with the IGS Infrastructure Committee. We highly appreciate your help and guidance throughout this process.
I would also like to share some news about our network infrastructure.
Today we launched, in test mode, a new service for collecting and distributing RINEX files:
https://cors.qgeo.kz/corsmonitor
For demonstration purposes, you may use the account:
Username : viewer
Password : %Pw%sG:N>2wg;@6
This account has read-only access.
In the coming days, I am planning to deploy the IGS SiteLog Manager 2.0 on the same server for our network. Until now, we have only used this system within our corporate local network.
We believe these services will make future data exchange and station management much easier and will help us align our infrastructure with IGS requirements.
Thank you again for your support and interest in our stations.

[4:23 PM] **Rui Fernandes:** I am preparing now a report just based on the visual inspection of the stations… But the access to the data can permit further tests…

[4:32 PM] **Вы:** Just a small note: the service is currently in a testing phase. Most core functionality is already working, but we are still refining some features and fixing minor issues.

[4:38 PM] **Вы:** I am currently reviewing the stations selected by @Lelyakov Anatoliy .
I am reprocessing the data by:
1. Replacing RINEX 2 files with RINEX 3 files when available.
2. Filling data gaps and replacing incomplete files.
The work for 2025 is already finished, and 2024 is partly completed. After that I will process 2023 and then the available data from 2022.

[4:42 PM] **Вы:** After this review is finished, we will be able to decide which stations should be processed and how to analyse their stability.
Earlier, you kindly offered to help by processing some stations with GypsyX or by providing a demo version of MIRA Series. This is exactly what I am preparing the data for now.

[4:48 PM] **Rui Fernandes:** Hi Roman,
Thank you very much for all your effort and for the detailed update. We'll be glad to wait for the updated information once your review is finished, and then decide together which stations to process and how to analyse their stability.
We also noticed it's not currently possible to download any data, but the site looks really great for presenting the metadata information.
As mentioned, we remain happy to help by processing some stations with GipsyX or by providing a demo version of MIRA Series — just let us know once the data is ready.
Thank you again.

[4:57 PM] **Вы:** Yes, there are several access levels in the system. For now, I shared the viewer account because I am still discussing some internal and legal aspects of data access with our management.
Personally, I fully support open access to CORS data and understand that this is common international practice. However, as these services belong to our organisation, some decisions need to be approved internally before I can provide public access.
In any case, if this process takes longer than expected, I will prepare archives for the selected stations and provide access to the data by another method, so that the stability analysis can move forward without delay.

[5:20 PM] **Rui Fernandes:** Thank you, Roman, understood — it is reasonable that the internal approvals come first. I would be glad to sign any NDA if that helps.
One point to keep in mind: the IGS stations will require open data in any case, as that is an IGS requirement. For the remaining stations, the policy is your decision.

---

## June 18, 2026

[8:31 AM] **Вы:** Thank you, Rui.
Yes, I completely understand the IGS open data requirement.
By the way, the website address has changed slightly. Please use https://cors.qgeo.kz instead of the previous /corsmonitor URL.

[3:17 PM] **Вы:** Hello @Rui Fernandes ,
Could you please send me your email address? I'd like to create an account for you in the SiteLog Manager system.

[3:18 PM] **Rui Fernandes:** rui@segal.ubi.pt

[3:25 PM] **Вы:** https://slm.qgeo.kz
This is the SiteLog Manager for the Kazakhstan CORS Network.
@Lelyakov Anatoliy , @Omirzaq , @Жандос Абильдинов , I have created accounts for you as well.

[3:26 PM] **Вы:** @Rui Fernandes, your password has been sent via private message.

[6:10 PM] **Rui Fernandes:** We made a preliminary visual inspection of the CORS station photos and I am also sending a filtered set of images containing only the antenna, monument/mount, rooftop or outside-building views. I excluded photos of receivers, technical boxes and internal equipment.
Please note that this is only a visual inspection. It is useful to identify possible risks, but the final selection of the reference stations must be based mainly on the quality of the RINEX data and on the processing results. In particular, we need to check data completeness, cycle slips, multipath indicators, residuals, coordinate repeatability, and consistency between solutions.
A station may look good from the photos because it has open sky visibility, but the photos do not always show how the antenna is connected to the building. This is important, because a station installed on a stable pillar is very different from a station installed directly on a roof slab, side wall, mast, or older/tall building structure.

Preliminary visual inspection:
Station	Visual assessment	Comment
RBEY	Good sky visibility; pillar visible; tall building caution	One photo suggests the antenna is installed on top of a pillar. Main concern is the height of the building and possible building motion.
EIND	Good sky visibility; monument not confirmed	Open surroundings, but the photos do not show clearly whether the antenna is fixed to a stable pillar or to the roof/building structure.
RAKT	Good sky visibility; monument not confirmed; tall building caution	Similar open-sky situation, but no photo confirms if the antenna is on a pillar. The tall building also requires caution.
PZHT	Good sky visibility; monument not confirmed	Open-sky conditions appear acceptable, but no photo confirms if the antenna is fixed to a stable pillar.
DYRG	Good sky visibility; monument not confirmed	Open-sky conditions appear acceptable, but no photo confirms if the antenna is fixed to a stable pillar.
PUZK	Good sky visibility; monument not confirmed	Open-sky conditions appear acceptable, but no photo confirms if the antenna is fixed to a stable pillar.
TNIS	Monument connection unclear	The issue is not mainly the trees, which seem lower than the antenna. The main uncertainty is how the monument is connected to the building, and there is no clear access/view of the building structure.
FCKP	Caution: possible rooftop-side multipath	The antenna appears to be close to the side of the rooftop, which may introduce multipath. The actual quality must be checked from the data.
DBOZ	Caution: possible multipath from corrugated building	The main concern is the corrugated/metal building environment, which may increase multipath.
MKRJ	Caution: older building / monument unclear	The building appears older and the photos do not clearly show a stable monument connection.
NARS	Antenna visible; monument not confirmed	The antenna is visible, but the photos do not provide enough information about the monument/support and its connection to the structure.
MSAT	Monument/support unclear	The installation and connection to the building are not clear enough from the photos.
SSHB	Monument/support unclear	The photos are not sufficient to assess the monument connection and local environment.
LORA	Caution: local environment unclear	Possible local multipath or building effects; monument/support details should be confirmed.
MAKD	Insufficient visual information	The available photos are insufficient to confirm monument stability or antenna environment.

Summary from the visual inspection only:
* More promising visually, but still requiring data validation: RBEY, EIND, RAKT, PZHT, DYRG, PUZK
* Main uncertainty is monument/support connection: EIND, RAKT, PZHT, DYRG, PUZK, TNIS, NARS, MSAT, SSHB
* Specific multipath/building concerns: FCKP, DBOZ, LORA, MKRJ
* Insufficient information: MAKD

For the test processing, I would not exclude or select stations based only on these photos. The important step is to analyse the actual CORS RINEX data and then evaluate which stations provide the most stable and consistent results for the sample points. Only after this test can we define the best reference stations for each region of the full project.

[6:12 PM] **Rui Fernandes:** [Документ] Outside_Pics.zip

---

## June 25, 2026

[1:54 PM] **Rui Fernandes:** Dear Colleagues, there was a IC-IGS meeting this week and I renovated your interest in providing several stations to the IGS network!

---

## July 3, 2026

[11:21 AM] **Вы:** Dear @Rui Fernandes ,
I have approved access to RINEX data for you. I sent your account details in a private message.
I have not finished the full revision of the selected stations yet. I will send more detailed information in this chat later.
Also, I would like to inform you that I will be on vacation for 2 weeks, so I will not be able to work during this time.

[1:00 PM] **Rui Fernandes:** Thank you! Let me check the access and back to you!

---

## July 23, 2026

[6:46 PM] **Rui Fernandes:** [Документ] Dear All, I am sending you a preliminary report of the processing of the QGEO-KZ network. I have used the available data between June 2022 and now. Please, analyse it. I think that can assist you to select the best stations to be proposed for IGS.

[6:47 PM] **Rui Fernandes:** [Документ] QGEO-KZ.pdf

[6:47 PM] **Rui Fernandes:** Let me know if you have any questions - I will be pleased to clarify any doubts.

[7:26 PM] **Вы:** Dear, Rui. This is fantastic! You've done an invaluable job. We'll be reviewing the reports in detail soon and answering our questions. Thank you so much!

---

## August 3, 2026

[9:18 AM] **Вы:** Dear @Rui Fernandes ,
sorry for the delayed reply. Many of our team members have been on vacation or business trips, so we are only now able to properly review your report. We will study it in detail this week and come back to you with our comments, questions, and proposals. Thank you again for your excellent work and support!
