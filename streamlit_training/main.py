import streamlit as st
import numpy as np
import pandas as pd
from PIL import streamlit

st.title('Streamlit 入門')

st.write('Display Image')

img = Image.open("bone33.png")

#Trueで幅に合わせて表示してくれる
st.image(img,caption="bone",use_column_width=False)
# df = pd.DataFrame(
#     np.random.rand(100,2)/[50,50] + [35.69,139.70],
#     columns=['lat','lon']
# )

##axis 0→列 1→行
##st.table→静的
##st.dataframe ソートができる，表の大きさを指定できる
##st.write 

#st.dataframe(df.style.highlight_max(axis=1),width=500,height=500)

##bar_char 棒グラフ area_chart
#st.map(df)

""" 
# 章
## 節
### 項

'''python
import streamlit as st
import numpy as np
import pandas as pd
'''
"""
