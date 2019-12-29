import wolframalpha

WOLFRAM_API_KEY = "UGXQ9Y-8YU4PA35AP"

class Wolfram_API:
    errorMsg = ""

    def init(self, key):    #stores client key in class obj
        self.api_key = key
        self.client = wolframalpha.Client(self.api_key)

    def sendQuestion(self, question):
        try:
            self.result = self.client.query(question)
        except:
            self.errorMsg = "bad input"

    def returnAns(self):
        if self.errorMsg != "":
            return self.errorMsg

        try:
            answer = next(self.result.results).text
            return (answer)
        except:
            return "Sorry, I didn't understand your question."

