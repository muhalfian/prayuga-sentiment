#import needed.db_mysql as db_mysql
import helper.preprocessing as preprocessing
import analyzer.impress as impress;
import pandas as pd

# def analyzeSentiment(id):
# 	sql = "SELECT *	FROM apps_opinion WHERE real_value is not null and id_apps="+str(id)
#
# 	db_mysql.executeSql(sql);
# 	result = db_mysql.fetch('all');
#
# 	for data in result:
# 		idOpini     = data[0];
# 		idApps      = data[1];
# 		kalimat     = data[3];
# 		keyword     = preprocessing.do(kalimat);
# 		dataProcess = impress.play(keyword,idApps);
# 		sentiment   = dataProcess['sentiment'];
# 		print("==========================\n\nID: "+str(data[0])+"\n"+kalimat+"\n--Sentiment: "+str(sentiment)+"\n");
#
# 		# for view counting rule impressi
# 		recordCounting = preprocessing.recordCounting(dataProcess);
# 		arr_word       = recordCounting['arr_word'];
# 		arr_counwted    = recordCounting['arr_counted'];
# 		arr_score      = recordCounting['arr_score'];
# 		role_group     = recordCounting['role_group'];
#
# 		sql = '''UPDATE apps_opinion
# 				 SET sentiment=%d, arr_word="%s", arr_score="%s", arr_counted="%s", role_group='%s' WHERE id=%d''' % \
# 				 (sentiment,arr_word,arr_score,arr_counted,role_group,idOpini);
# 		db_mysql.executeSql(sql);
# 		db_mysql.commit();
#
# # for id in range(28, 37):
# 	analyzeSentiment(37)
# kalimat = "USER_MENTION waaa o USER_MENTION yang kelas jangan seneng dulu mau jadi kelas nanti pas ujian nasional lo kesel sendiri jadi kelas"


data = pd.read_json("data/3_class_labeled_tweet.json", lines=True)
print(data.shape)

for i in range(22,121):
    bawah = i*1000
    atas = (i+1)*1000

    if(i==120):
        data_process = data[bawah:]
    else:
        data_process = data[bawah:atas]

    sentiment_arr = []
    for key, row in data_process.iterrows():

        kalimat = row['tweets']
        keyword     = preprocessing.do(kalimat);
        # print(keyword)
        # print("================================")
        dataProcess = impress.play(keyword);
        # print(dataProcess)
        # print("================================")
        sentiment   = dataProcess['sentiment'];
        print(str(key) + " - [" + str(sentiment) + "] = " + row['tweets'])
        # print(sentiment)
        # print("================================")
        sentiment_arr.append(sentiment)

    print("SIMPAN DATA JSON "+ str(i))

    data_process['sentiment'] = sentiment_arr
    data_process.to_json("data/json/resentiment-"+str(i)+".json", lines=True, orient='records')
    data_process.to_csv("data/csv/resentiment-"+str(i)+".csv")
