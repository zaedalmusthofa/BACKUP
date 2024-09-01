import matplotlib.pyplot as plt

# Membuat figure
plt.figure()

# Menambahkan subplot di grid 2x2, posisi pertama
plt.subplot(2, 2, 1)
plt.plot([1, 2, 3], [1, 4, 9])
plt.title('Plot 1')

# Menambahkan subplot di grid 2x2, posisi kedua
plt.subplot(2, 2, 2)
plt.plot([1, 2, 3], [1, 2, 3])
plt.title('Plot 2')

# Menambahkan subplot di grid 2x2, posisi ketiga
plt.subplot(2, 2, 3)
plt.plot([1, 2, 3], [1, 0, -1])
plt.title('Plot 3')

# Menambahkan subplot di grid 2x2, posisi keempat
plt.subplot(2, 2, 4)
plt.plot([1, 2, 3], [1, 3, 5])
plt.title('Plot 4')

# Menampilkan plot
plt.tight_layout()
plt.show()
