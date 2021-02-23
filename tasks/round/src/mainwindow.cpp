#include <QMouseEvent>
#include <QVector>
#include <QDebug>
#include <QFontMetrics>
#include <QFontDatabase>
#include <QTimer>
#include <QtMath>
#include <stdexcept>
#include <list>

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "flag.h"

static constexpr int padding = 1;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setWindowFlags(Qt::Window | Qt::FramelessWindowHint);
    this->setFixedSize(this->size());
    QRegion region(QRect(0, 0, this->width(), this->height()), QRegion::Ellipse);
    this->setMask(region);
    this->roundFun();
}

MainWindow::~MainWindow()
{
    delete ui;
}

std::vector<MainWindow::LabelInfo> MainWindow::createLabels(const QFont &font)
{
    QFontMetrics metrics(font, this);
    int charWidth = metrics.horizontalAdvance('_');
    float center = (float)this->height() / 2;

    qDebug() << "center" << center << charWidth << metrics.height();

    auto computeLabel = [&](int position) -> std::optional<std::pair<int, QRect>> {
        float angleSin = (center - (position + metrics.height())) / center;
        float angleCos = qSqrt(1 - (angleSin * angleSin));
        float yPos = center * (1 - angleCos);
        int controlWidth = yPos - padding;
        int chars = controlWidth / charWidth;
        qDebug() << position << angleSin << angleCos << yPos << controlWidth << chars;
        if (chars > 0) {
            return std::optional(std::make_pair(chars, QRect(padding, position, controlWidth, metrics.height())));
        } else {
            return std::nullopt;
        }
    };

    // First -- calculate one side.
    std::vector<std::pair<int, QRect>> leftSide;
    int position = padding;
    while (position < center - metrics.height()) {
        auto label = computeLabel(position);
        if (label) {
            leftSide.emplace_back(*label);
        }
        position += metrics.height();
    }
    // I'm too lazy to do this efficiently.
    std::vector<std::pair<int, QRect>> lowerLeftSide;
    position = this->height() - padding - metrics.height();
    while (position > center) {
        auto label = computeLabel(position);
        if (label) {
            lowerLeftSide.emplace_back(*label);
        }
        position -= metrics.height();
    }
    leftSide.insert(leftSide.end(), lowerLeftSide.rbegin(), lowerLeftSide.rend());

    // Now build final "clock" of labels.
    std::vector<LabelInfo> res;
    for (const auto& label : leftSide) {
        res.emplace_back(LabelInfo {
             .chars = label.first,
             .rect = QRect(QPoint(this->width() - label.second.x() - label.second.width(), label.second.y()), label.second.size()),
             .right = true,
         });
    }
    for (auto i = leftSide.rbegin(); i != leftSide.rend(); i++) {
        const auto& label = *i;
        res.emplace_back(LabelInfo {
             .chars = label.first,
             .rect = label.second,
             .right = false,
         });
    }
    return res;
}

void MainWindow::renderRoundText(const QString &text, int maxChars)
{
    int pos = 0;
    for (auto& label : this->labels) {
        int labelChars = qMin(label.first, text.size() - pos);
        if (maxChars >= 0) {
            labelChars = qMin(maxChars, labelChars);
        }
        QStringRef textPart(&text, pos, labelChars);
        label.second->setText(textPart.toString());
        pos += textPart.size();
    }
    if (pos < text.size()) {
        throw std::runtime_error("Failed to render");
    }
}

void MainWindow::mouseMoveEvent(QMouseEvent *event)
{
    if (this->prevPos) {
        this->move((event->globalPos() - *this->prevPos).toPoint());
    }
}

void MainWindow::mousePressEvent(QMouseEvent *event)
{
    if (event->buttons() & Qt::LeftButton) {
        this->prevPos = event->windowPos();
    }
}

void MainWindow::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->buttons() & Qt::LeftButton) {
        this->prevPos = std::nullopt;
    }
}

void MainWindow::roundFun()
{
    auto font = QFontDatabase::systemFont(QFontDatabase::FixedFont);
    font.setPixelSize(15);
    qDebug() << "size" << font.pixelSize();
    auto labelSizes = this->createLabels(font);
    for (const auto &labelInfo : labelSizes) {
        qDebug() << "Adding label" << labelInfo.chars << labelInfo.rect << labelInfo.right;
        auto label = new QLabel(this);
        label->setFont(font);
        label->setGeometry(labelInfo.rect);
        if (labelInfo.right) {
            label->setAlignment(Qt::AlignRight);
        }
        this->labels.emplace_back(labelInfo.chars, label);
    }
    auto flag = get_flag();
    qDebug() << "flag" << flag;
    QString flagStr(flag);
    free(flag);
    //QString flagStr = QString("a").repeated(this->labels.size());
    qDebug() << "string size" << flagStr.size();
    this->renderRoundText(flagStr, 1);
}
