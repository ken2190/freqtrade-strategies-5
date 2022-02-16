def PMAX(dataframe, period, multiplier,length):
    start_time = time.time()

    df = dataframe.copy()
    last_row = dataframe.tail(1).index.item()

    mavalue = 'MA_' + str(length)
    df[mavalue] = ta.EMA(df , length)
    df['ATR'] = ta.ATR(df, period)

    pm = 'PM_' + str(period) + '_' + str(multiplier)
    pmx = 'PMX_' + str(period) + '_' + str(multiplier)

    # Compute basic upper and lower bands
    BASIC_UB = (df[mavalue] + multiplier * df['ATR']).values
    BASIC_LB = (df[mavalue] - multiplier * df['ATR']).values
    FINAL_UB = np.zeros(last_row + 1)
    FINAL_LB = np.zeros(last_row + 1)
    PM = np.zeros(last_row + 1)
    MAVALUE = df[mavalue].values

    # Compute final upper and lower bands
    for i in range(period, last_row):
        FINAL_UB[i] = BASIC_UB[i] if BASIC_UB[i] < FINAL_UB[i - 1] or MAVALUE[i - 1] > FINAL_UB[i - 1] else FINAL_UB[i - 1]
        FINAL_LB[i] = BASIC_LB[i] if BASIC_LB[i] > FINAL_LB[i - 1] or MAVALUE[i - 1] < FINAL_LB[i - 1] else FINAL_LB[i - 1]

    # Set the Pmax value
    for i in range(period, last_row):
        PM[i] = FINAL_UB[i] if PM[i - 1] == FINAL_UB[i - 1] and MAVALUE[i] <= FINAL_UB[i] else \
                FINAL_LB[i] if PM[i - 1] == FINAL_UB[i - 1] and MAVALUE[i] >  FINAL_UB[i] else \
                FINAL_LB[i] if PM[i - 1] == FINAL_LB[i - 1] and MAVALUE[i] >= FINAL_LB[i] else \
                FINAL_UB[i] if PM[i - 1] == FINAL_LB[i - 1] and MAVALUE[i] <  FINAL_LB[i] else 0.00
    df_PM = pd.DataFrame(PM, columns=[pm])
    df = pd.concat([df, df_PM],axis=1)

    # Mark the trend direction up/down
    df[pmx] = np.where((df[pm] > 0.00), np.where((df['close'] < df[pm]), 'down',  'up'), np.NaN)

    df.fillna(0, inplace=True)

    end_time = time.time()
    # print("total time taken this loop: ", end_time - start_time)

    return df