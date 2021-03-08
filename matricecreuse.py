class MatriceCreuse:

    def __init__(self, L = [0], C = [], I = []):
        self.L = L.split("\n")
        self.C = C.split("\n")
        self.I = I.split("\n")
        self.L.pop()
        self.C.pop()
        self.I.pop()


    def trM_x_V(self, V):
        result = [0]*len(V)
        lenl = len(self.L)
        s=0
        """print(self.L.rstrip(self.L[-1]))"""
        for i in range(lenl-1):
            if self.L[i]== self.L[i+1]:
                s=s+V[i]

            for a in range(int(self.L[i]), int(self.L[i+1])):
                result[int(self.I[a])] += float(self.C[a])*V[i]

        s=s/(lenl-1)
        d=1/7
        for i in range(lenl-1):
            result[i] = (d/(lenl-1)) + (1 - d)*(result[i]+s)
            
        return result

    def find_nb_colonne(self):

        return len(self.L) - 1


    #pagerank_zap
    def pagerank_zap(self):

        Z= [1/self.find_nb_colonne()]*self.find_nb_colonne()
        print(Z)
        for i in range(50):

            Z1 = self.trM_x_V(Z)
            Z = Z1

        return Z
