#ifndef ANALOGCLOCK_H
#define ANALOGCLOCK_H

#include <QWidget>

class AnalogClock : public QWidget
{
    Q_OBJECT

public:
    AnalogClock(QWidget *parent = nullptr);

protected:
    void paintEvent(QPaintEvent *event) override;
};

#endif // ANALOGCLOCK_H
