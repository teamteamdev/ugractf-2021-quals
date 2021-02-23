#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>
#include <vector>
#include <memory>
#include <optional>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    struct LabelInfo
    {
        int chars;
        QRect rect;
        bool right;
    };

    Ui::MainWindow *ui;
    std::optional<QPointF> prevPos;
    std::vector<std::pair<int, QLabel*>> labels;

    bool initialized = false;
    std::vector<LabelInfo> createLabels(const QFont &font);
    void renderRoundText(const QString &text, int maxChars = -1);
    void roundFun();

protected:
    void mouseMoveEvent(QMouseEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
};
#endif // MAINWINDOW_H
