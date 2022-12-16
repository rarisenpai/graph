import stats_can
import pandas as pd
import streamlit as st
from datetime import datetime
import hvplot
import hvplot.pandas

def gettingVectorsForGraphing(listOfVectors, df):
    if 'nameOfOutputFile' in locals():
        dataSource = nameOfOutputFile

        def load_data():
            data = pd.read_csv(dataSource, parse_dates=['refPer'])
            data['refPer'] = pd.to_datetime(data['refPer']).dt.strftime('%Y-01-01')
            return data

        df = load_data()

        # show data on streamlit
        st.write(df)

        # Filters UI

    subset_data = df
    vectorColsSubset =     st.sidebar.multiselect('VectorCols', listOfVectors, on_change=gettingVectorsForGraphing,
                                                      args=(listOfVectors, df,))
    st.session_state.vectorColsSubset = vectorColsSubset
    runOnce = True

    if len(vectorColsSubset) > 0:
        vectorColsSubsetOriginal = vectorColsSubset
        vectorColsSubset.append('refPer')
        subset_data = df[df.columns.intersection(vectorColsSubset)]
        if 'refPer' in vectorColsSubsetOriginal:
            vectorColsSubsetOriginal.remove('refPer')
        st.write(subset_data)
        subset_data.sort_values(by='refPer', ascending=True)
        st.subheader('Graphing Columns of Data')
        st.write(f'subsetvector:{vectorColsSubsetOriginal}')
        hvChart = df.hvplot(x='refPer', y=vectorColsSubsetOriginal)
        st.bokeh_chart(hvplot.render(hvChart, backend='bokeh'))

listOfVectors = []
st.title("Stats Can Simplified")
# save the input text in the variable 'name'
# first argument shows the title of the text input box
# second argument displays a default text inside the text input area

if 'runOnce' not in locals():
    vector = st.text_input("the vector you would like to combine separated by a comma", "Type Here ...")


    if st.button('Submit'):
        st.session_state.buttonClicked = True
        st.session_state.vector = vector
        vector = vector.replace(" ", "")
        comma = ','
        if comma in str(vector):
            arrayOfVectors = vector.split(",")
            for item in arrayOfVectors:
                st.text(f'{item}, vector: {vector}')
                listOfVectors.append(item)
            result = vector.title()
            st.success(result)
            st.text(f"Working On It{listOfVectors} {type(arrayOfVectors)}")
        elif vector:
            st.text(f"elif Statement{vector} {type(vector)} list of vectors value: {listOfVectors}")
            listOfVectors.append(vector)
        st.session_state.listOfVectors = listOfVectors



        df = pd.DataFrame()

        for vector in listOfVectors:

            dfNew = stats_can.sc.vectors_to_df(str(vector.upper()), start_release_date = '1976-01-01', end_release_date = '2022-01-31')
            print(dfNew)
            if not df.empty:
                df = pd.merge(df, dfNew, on='refPer', how='outer')

            else:
                df = stats_can.sc.vectors_to_df(str(vector.upper()), start_release_date = '2017-01-01', end_release_date = '2022-01-31')
                #df.index.names = ['Date']

        if not df.empty:
            st.session_state.df = df
            nameOfOutputFile = 'statsCanData.csv'
            st.session_state.nameOfOutputFile = nameOfOutputFile
            df.to_csv(nameOfOutputFile)

if 'df' in locals():
    st.sidebar.multiselect('VectorCols', listOfVectors, on_change=gettingVectorsForGraphing,
                                                      args=(listOfVectors, df,))



