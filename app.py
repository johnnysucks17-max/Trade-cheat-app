import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.title("Trade Cheat")
st.warning("Rough guess only. Not advice. No app can predict markets exactly.")

mins = st.number_input("How many minutes does your screenshot show?", 5, 1440, 60)
file = st.file_uploader("Upload chart screenshot", type=["png", "jpg", "jpeg"])

if file:
    img = Image.open(file).convert("L")
    img.thumbnail((600, 400))
    a = np.array(img).astype(float)
    diff = np.abs(a - np.median(a))
    xs, ys = [], []
    for x in range(a.shape[1]):
        col = diff[:, x]
        if col.max() > 40:
            xs.append(x)
            ys.append(a.shape[0] - col.argmax())
    if len(xs) < 20:
        st.error("Could not read the chart. Try a clearer screenshot.")
        st.stop()
    xs = np.array(xs)
    ys = np.array(ys)
    n = max(10, len(xs) // 4)
    slope, inter = np.polyfit(xs[-n:], ys[-n:], 1)
    steps = max(5, int(len(xs) * 30 / mins))
    fx = np.arange(xs[-1], xs[-1] + steps)
    fy = slope * fx + inter
    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="Your chart")
    ax.plot(fx, fy, "--", color="orange", label="Next 30 min (rough guess)")
    ax.legend()
    st.pyplot(fig)
    st.caption("This is a simple trend guess, not a promise.")
