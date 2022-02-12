import ktrain
from sklearn.datasets import fetch_20newsgroups

remove = ('headers', 'footers', 'quotes')
data = fetch_20newsgroups(subset='train', remove=remove)
# print("data:", data)

texts = data.data
targets = data.target
target_names = data.target_names

print("data.target: ", data.target)
print("data.target_names: ", data.target_names)
print("len(texts): ", len(texts), ", len(targets): ", len(targets))

categories = [target_names[target] for target in targets]

print("target_names: ", categories)

tm = ktrain.text.get_topic_model(texts, n_features=10_000)
tm.build(texts, threshold=0.25)

tm.filter(texts)
categories = tm.filter(categories)

tm.print_topics(show_counts=True)

tm.visualize_documents(doc_topics=tm.get_doctopics(), filepath="visualization.html")

doc_topics = tm.get_doctopics(topic_ids=[31, 55])
tm.visualize_documents(doc_topics=doc_topics, filepath="visualization_topic_31_55.html")

news = news = """elon mask has come with an idea to explore the space and universe"""

pred = tm.predict([news])

print("tm.predict([news]): ", pred)