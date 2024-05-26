## SSIM的技术路线是否可行？
- 考虑10000张级别的数据库 这样的算法的时间复杂度是否可以接受？
- Structural Similarity Index, SSIM
  - 公式：$SSIM(x,y) = \frac{(2\mu_x\mu_y + c_1)(2\sigma_{xy} + c_2)}{(\mu_x^2 + \mu_y^2 + c_1)(\sigma_x^2 + \sigma_y^2 +c_2)}$
  - 其中:
    - $x$和$y$是两张图片的局部窗口。
    - $\mu_x$和$\mu_y$是$x$和$y$的平均值。
    - $\sigma_x^2$和$\sigma_y^2$是$x$和$y$的方差。$\sigma_{xy}$是$x$和$y$的协方差。
    - $c_1$和$c_2$是为了防止分母为0的常数，通常取值为$c_1=(k_1L)^2$，$c_2=(k_2L)^2$，其中$L$是像素的动态范围（例如，对于8位图像，$L=255$)，$k_1=0.01$,$k_2=0.03$。
    - SSIM的值范围是[-1，1]，值越接近1，表示两张图片越相似。
- 在Python中，获取文件扩展名可以使用`os.path.splitext()`函数，它是`os.path`模块提供的一个方法。这个函数会将文件名分解为两部分：文件名和扩展名，并返回一个包含这两部分的元组。扩展名部分包括点（`.`）。
  - 以下是如何使用`os.path.splitext()`来获取文件扩展名的示例：
```python
import os

# 假设我们有一个文件路径
file_path = '/path/to/your/file.txt'

# 使用os.path.splitext()获取文件扩展名
file_name, file_extension = os.path.splitext(file_path)

# 打印结果
print(f"文件名: {file_name}")
print(f"扩展名: {file_extension}")
```

-在上面的例子中，`file_name`将包含`/path/to/your/file`，而`file_extension`将包含`.txt`。

如果你想要获取扩展名并去除点，可以简单地去掉扩展名字符串的第一个字符：

```python
# 获取扩展名（不含点）
file_extension = file_extension[1:]
print(f"扩展名（不含点）: {file_extension}")
```

另外，从Python 3.4开始，`pathlib`模块提供了一种面向对象的方式来处理文件系统路径。使用`pathlib`来获取文件扩展名的示例如下：

```python
from pathlib import Path

# 创建Path对象
file_path = Path('/path/to/your/file.txt')

# 获取文件扩展名
file_extension = file_path.suffix

# 打印结果
print(f"扩展名: {file_extension}")
```

使用`pathlib`的好处是它可以提供更直观和面向对象的方式来处理文件路径和相关操作。


