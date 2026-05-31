"""会议效果评估器"""


class MeetingEvaluator:
    """会议效果评估器，分析会议的效率、决策产出和行动项完成情况。"""

    def __init__(self, title: str):
        """初始化会议评估器。

        Args:
            title: 会议标题
        """
        self.title = title
        self.participants = []
        self.agenda = []
        self.duration_minutes = 0
        self.decisions = []
        self.action_items = []

    def set_duration(self, minutes: int):
        """设置会议时长。

        Args:
            minutes: 会议时长（分钟）

        Returns:
            返回自身以支持链式调用
        """
        self.duration_minutes = minutes
        return self

    def add_participant(self, name: str, role: str = "成员"):
        """添加参会人员。

        Args:
            name: 参会人姓名
            role: 参会人角色，如"主持人"、"产品经理"

        Returns:
            返回自身以支持链式调用
        """
        self.participants.append({"name": name, "role": role})
        return self

    def add_agenda(self, item: str, duration: int):
        """添加议程项。

        Args:
            item: 议程内容描述
            duration: 计划时长（分钟）

        Returns:
            返回自身以支持链式调用
        """
        self.agenda.append({"item": item, "planned": duration})
        return self

    def add_decision(self, decision: str):
        """记录会议决策。

        Args:
            decision: 决策内容描述

        Returns:
            返回自身以支持链式调用
        """
        self.decisions.append(decision)
        return self

    def add_action(self, task: str, owner: str, deadline: str):
        """添加行动项（待办任务）。

        Args:
            task: 任务描述
            owner: 负责人姓名
            deadline: 截止日期，格式"YYYY-MM-DD"

        Returns:
            返回自身以支持链式调用
        """
        self.action_items.append({
            "task": task, "owner": owner,
            "deadline": deadline, "status": "待处理",
        })
        return self

    def evaluate(self) -> dict:
        """评估会议效果并生成评分报告。

        Returns:
            评估结果字典，包含时长、参与人数、效率评分、结论等
        """
        efficiency = min(100, max(0, 100 - max(0, len(self.agenda) * 10 - self.duration_minutes)))
        decision_rate = len(self.decisions) / max(len(self.agenda), 1)
        action_rate = len(self.action_items) / max(len(self.agenda), 1)

        return {
            "会议标题": self.title,
            "时长": f"{self.duration_minutes}分钟",
            "参与人数": len(self.participants),
            "议程完整度": f"{len(self.agenda)}项",
            "决策数": len(self.decisions),
            "行动项": len(self.action_items),
            "效率评分": f"{efficiency}/100",
            "评分等级": "优秀" if efficiency >= 80 else "良好" if efficiency >= 60 else "待改进",
            "结论": self._recommendation(efficiency),
        }

    def _recommendation(self, score: int) -> str:
        """根据效率评分生成改进建议。

        Args:
            score: 效率评分（0-100）

        Returns:
            改进建议文本
        """
        if score >= 80:
            return "高效会议，继续保持"
        elif score >= 60:
            return "整体良好，可减少参会人数或缩短时长"
        return "需要优化：控制议程长度，提前发送资料"


if __name__ == "__main__":
    eval = MeetingEvaluator("Q2产品规划评审")
    eval.set_duration(45) \
        .add_participant("张三", "主持人") \
        .add_participant("李四", "产品经理") \
        .add_participant("王五", "技术负责人") \
        .add_agenda("Q2目标回顾", 10) \
        .add_agenda("新功能评审", 20) \
        .add_agenda("资源分配", 10) \
        .add_agenda("Q&A", 5) \
        .add_decision("优先开发用户增长模块") \
        .add_decision("延期支付系统优化") \
        .add_action("撰写PRD", "李四", "2026-06-05") \
        .add_action("技术方案评审", "王五", "2026-06-10")
    for k, v in eval.evaluate().items():
        print(f"{k}: {v}")
