### **Workflow**
1. **HTML Producer** (`HtmlProducer`)  
   - Reads **HTML files** and sends them as messages to **Kafka topic `html_topic`**.
   
2. **HTML Consumer** (`HtmlConsumer`)  
   - Listens to `html_topic` and extracts structured **pages** from HTML content.
   - Sends extracted **pages** to Kafka topic `person_topic`.
   
3. **Person Consumer** (`PersonConsumer`)  
   - Listens to `person_topic`, validates the extracted data, and stores it in **MongoDB**.

---

## **Architecture**
```plaintext
HtmlProducer
--->  Kafka (html_topic)  --->  HtmlConsumer (extracts pages)
--->  Kafka (person_topic)  --->  PersonConsumer (validates & stores in MongoDB)
