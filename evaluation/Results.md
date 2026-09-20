 ## Results
 
 Profiles tested: 10        

Top-1 Accuracy:  50%   (5/10)       
Top-3 Accuracy: 100%  (10/10)       
Top-5 Accuracy: 100%  (10/10)       
 
 #### What this tells us about Growvia

That means the model is fairly good at getting a sensible role somewhere near the top,      
 but it is not reliable enough yet to treat the first role as “the answer.”     

This actually supports the idea that: DeBERTa alone probably shouldn't determine the final role ranking.        
 
 The eventual system could look more like:
 
                    CV
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    DeBERTa       Skills      Semantic
   role score    evidence     similarity
        │            │            │
        └────────────┼────────────┘
                     ↓
             Role Recommendation
                     ↓
               Top 3 roles