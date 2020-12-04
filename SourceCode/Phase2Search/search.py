from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.query import *
import os.path, json
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring, searching

JSONFILENAME = "TotalIdeaData.json" # Put path to JSON file here

schema = Schema(title=TEXT(stored=True), Challenge=TEXT, problemStatement=TEXT, description=TEXT(stored=True),
    path=ID, tags=KEYWORD)

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)

ix = open_dir("index")

writer = ix.writer()

#Load data from Json file into ideaList variable
with open(JSONFILENAME, "r") as readit: 
    ideaList = json.load(readit) 

#Load data into
for idea in ideaList:
    ideaBody = idea["body"]
    writer.add_document(
        title=ideaBody["Title"], 
        #Did not include challenge yet because not all ideas contain the challenge section
        problemStatement=ideaBody["problemStatement"], 
        description=ideaBody["Description"],
        path=u"/a", tags=u"can insert tags here")

writer.commit()

querystring = input("Enter your search query: ")

with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
    parser = QueryParser("description", ix.schema)
    myquery = parser.parse(querystring)
    results = searcher.search(myquery)
    print("We found ", len(results), "matches to your query")
    for result in results:
        print()
        print("Title:", result["title"])
        print("Description:", result["description"])
        print()
    print()
    docnum = searcher.document_number(path=u"/a")
    r = searcher.more_like(docnum, "description")
    print("Documents like: ", searcher.stored_fields(docnum)["title"])
    for hit in r:
        print("-", hit["title"])


# writer.add_document(title=u"How Red Bull can use social media?", 
#                     problemStatement="How Red Bull can use social media?\r\n\r\nEvery company that wants to create a successful marketing campaign needs a social media presence and Red Bull knows that. Red Bull Media House is a great company but you also need social media content, communication, and a social media strategy.\r\n\r\nTheir strategy is ingenious but at the same time simple:\r\n\r\nFirst, they trigger consumer engagement through inspirational videos and activities.\r\nThese activities lead to videos and images that sometimes become viral. However, the brand is always prominent.\r\nThe next step is to create brand recognition through logo saturation and of course, clever product placements during sports events.\r\nThe result is widespread brand recognition and loyalty among a specific demographic group followed by new campaigns that aim to other groups as well.\r\nThrough their media companies, they produce content.\r\n\r\nWhat about their presence on social media? What types of content do they share with their fans and customers?", 
#                     description=u"Facebook: More than 48 million people liked Red Bull’s Facebook page. This is an impressive number even for a big corporation but nothing is at random when it comes to this company. Their shared content is focused on video but it is a mix of entertaining and informative content.\r\n\r\nTheir slogan is reflected in everything they share with their fans, including the amazing pictures posted on their Facebook wall.\r\n\r\nIf you follow their page you can easily notice that everything is true: Red Bull really gives you wings.\r\n\r\nActionable tips you can learn to optimize your Facebook page:\r\n\r\nThey are very responsive withing their message – that means that Red Bull social media team is responding at almost every private message in the fastest way they could\r\nThey are also using .gif’s to comment and create a human-based Facebook profile\r\nInteract with their community – The Red Bull Facebook page is not a distribution page, it’s a community page where people engage with each other\r\n\r\nTwitter: There are significantly fewer followers on Twitter than on Facebook but it is understandable, considering that this social platform is not as popular as it was a few years ago. Here, the content is based on a mix of videos and images based on speed, sports, and motion.\r\n\r\nTheir captions are short but at the same time, captivating.\r\n\r\nInstagram: Similarly to their Twitter presence, Red Bull’s Instagram posts are a mix of videos and images. However, behind every image, there is a story to be told and we can always expect something really cool and exciting from Red Bull when it comes to digital content. Also Red Bull is playing the UGC game on their Instagram, giving the audience a much larger perspective about the sport and athletes.\r\n\r\nInstagram is not only for posting videos and images, they also ask their community to vote the next photo to publish on their feed using Instagram Stories.\r\n\r\nYouTube: This is the social media channel where Red Bull has something really special to share with their fans. There are more than 6 million subscribers who are enjoying daily video uploads.\r\n\r\nThe content is diverse so that it will appeal to different audiences.\r\n\r\nThe important fact is that through their YouTube channel we get to know Red Bull, their core values, what do they stand for and what motivates them but we can also get to know sports personalities and daring people who adhere to the company’s values and messages.",
#                     path=u"/a", tags=u"can insert tags here")
# writer.add_document(title=u"Fuel from the sea", 
#                     problemStatement="Thomas Hinderling was a man ahead of his time. A nuclear physicist and CEO of the Swiss Centre for Electronics and Microtechnology (CSEM, he was the brains behind solar islands and, one year before his death, founded Novaton with his wife Christine Ledergerber-Hinderling, who today carries on his legacy.\r\nWhile the whole world was still blithely praising oil, gas and nuclear power, Hinderling already believed in the power of the sun and invented solar islands that extract the greenhouse gas carbon dioxide from the sea and convert it into methanol fuel in a chemical process, thereby supplying energy.\r\nHe was \"ridiculed by many as a lunatic\", according to his wife, who also described him as an \"a unifying figure, a researcher, a visionary, someone who wanted to shape our future for the better – a philanthropist.\"",
#                     description=u"Novation came to fruition in 2010, a year before his death. The company's solar-powered islands use desalinization and electrolysis to extract hydrogen and carbon dioxide from the water in order to create methanol, which is pumped into a neighboring ship to take back to land.\r\nLedergerber-Hinderling is hopeful that the first island, which could supply thousands of households, will be launched at one of three possible locations: the Persian Gulf, the coast of South Asia, or northern Australia, aiming for spots where the waves are not too high and hurricanes are rare.",
#                     path=u"/b", tags=u"can insert tags here")
# writer.add_document(title=u"Corporate Companies Investing In Young Entrepreneurs", 
#                     problemStatement="Red Bull kicked off its first-ever Innovation Summit last weekend in New York City, bringing together a handful of collegiate entrepreneurs for a three-day workshop designed to help hone their investor pitch and further develop their business ideas. In attendance were the co-founders of an Austin-based ride-share app, Krew; an online clothing platform that helps girls choose party outfits, Swayy; and Cy5, a biometric temporary tattoo. The students, who are from the University of Texas at Austin and Wichita State University, respectively, were selected from a pool of 140 applicants.",
#                     description=u"Tech conferences may be the next place you’ll spot big brands out to woo young entrepreneurs.\r\n\r\nRed Bull, the 34-year-old energy drink company with a brand value of $10.4 billion, is as famous for its extravagant sponsorships of racing cars, EDM festivals and a splashy 2012 supersonic freefall into New Mexico as it is for the energizing beverages. But now it’s quietly but increasingly been making its way into the startup scene.\r\n\r\nIt certainly isn’t the only corporate company taking startups seriously. From L’Oreal’s Women in Digital NEXT Generation program to Kaplan’s EdTech Accelerator, various companies have begun to invest heavily in entrepreneurship in recent years.",
#                     path=u"/b", tags=u"can insert tags here")
# writer.add_document(title=u"Crowdsourcing product ideas to be manufactured", 
#                     Challenge=u"Electric Cars/Impact on Convenience Stores",
#                     problemStatement=u"You might have heard about Quirky, a community-led invention platform. The concept behind Quirky is that you can put your product idea up on Quirky and others within the Quirky community can comment and contribute to your idea.\r\n\r\nIf the idea is good and gains traction, it can be developed further by people on Quirky. ",
#                     description=u"Quirky members have a wide range of special skills, so you can collaborate with those that complement your expertise. Thus, the ready product is developed by the community.\r\n\r\nThe best products on the platform are chosen by Quirky for manufacturing and sold at the Quirky store. The process at this point is financed by Quirky, so having your own company and resources isn’t crucial for your product’s success.\r\n\r\nBut why would people share their expertise and develop ideas that are then manufactured and sold by Quirky?\r\n\r\nYou can get your product idea out there with much less effort. If you  want to make your idea a reality, Quirky offers a simple way to do so.\r\n\r\nYou can learn and get to use your talent to acquire more experience to put to your CV, and perhaps be one step closer to your dream job.\r\n\r\nIf the product ends up being a success you can earn money from being part of developing it. If the idea is originally yours, you may get royalties depending upon its success. This is what makes Quirky an active platform with an active community.\r\n\r\nPractical takeaways \r\nThe practical teaching from the Quirky example is that there is a way to get people ideating for you even for free.\r\n\r\nBy assessing problems that many have to deal with or by creating challenging tasks, people get motivated to collaborate with you. To cultivate this collaboration and create an active community, an appealing online presence will go a long way to make sure people find you.\r\n\r\nEven though you might recognize Samsung from several plagiarism case convictions, Samsung has also been qualified as one of the most innovative big companies today. Of course, Samsung has a major internal R&D unit, but the company is also a proud open innovation advocate and does open innovation collaboration especially with startups.\r\n\r\nThe distinctive part of Samsung’s open innovation collaboration is that Samsung divides it to 4 categories.\r\n\r\nThe four categories are even described as being the \"four legs of the open innovation activities\" at Samsung.\r\n\r\nThe 4 categories of collaboration:\r\n\r\nPartnerships\r\nVentures\r\nAccelerators\r\nAcquisitions\r\nPartnerships are essentially collaboration between companies, such as startups in Silicon Valley. Typically partnerships aim for new features or integrations within Samsung’s existing products. \r\n\r\nVentures can be described as investments into early stage startups. These investments can bring revenue in case of exits, but also provide access to new technologies that Samsung can learn and benefit from. For example, Samsung has invested in Mobeam, a mobile payment company.\r\n\r\nAccelerators provide startups with an innovative and empowering environment to create new things. Samsung offers these startups an initial investment, facilities to work in, as well as some resources from their vast pool. The idea is that the products stemming from the internal startups could become a part of Samsung’s product portfolio over time or just serve as learning experiences for the company.\r\n\r\nAcquisitions aim to bring in startups working on innovations that are at the core of Samsung's strategic areas of the future. These acquisitions often remain independent units and can even join the Accelerator program.\r\n\r\n\r\nCollaboration with Startups\r\n\r\nAs an example of Samsung’s collaboration with startups, Samsung has acquired an IoT company called SmartThings to gain an IoT platform without having to spend the money, and time on R&D.\r\n\r\nSamsung sees potential in the IoT industry and views it as a strategically important part of their future business and thus an area where they want to be forerunner.\r\n\r\nSmartThings still continues to operate as an independent startup fueled with the resources of a big company. With the investment, potential and home electronics of Samsung, SmartThings can really be developed into an integral part of Samsung products, by creating new IoT possibilities for homes.",
#                     path=u"/c", tags=u"can insert tags here")