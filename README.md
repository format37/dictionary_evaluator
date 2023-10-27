### Dictionary evaluator
This can be used to improve the speech dictionary.  
1. Make a voice conversation with the Chat-GPT mobile.
2. Sent this message to the Chat-GPT assistant:
```
Please, 
1. Collect all my speech in a single text variable
2. Collect all your speech in another text variable
```
3. Save each text to files:
```
user.txt
assistant.txt
```
4. Run the evaluator:
```
python3 evaluator.py
```
5. The evaluator will create 3 files:
```
Words Exclusively Spoken by User.png
Words Exclusively Spoken by Assistant.png
assistant_only.txt
```
In addition, the user's unique word count will be printed to the console:
```
Count of overall words that persist in the user's text: 72
Count of words that persist only in the assistant's text: 53
```
You can use this as a metric to improve the speech dictionary. And you can choose the words in the assistant_only.txt file to learn them for use in further speech.  
[!Words Exclusively Spoken by Assistant](assets/Words%20Exclusively%20Spoken%20by%20Assistant.png)  
[!Words Exclusively Spoken by User](assets/Words%20Exclusively%20Spoken%20by%20User.png)