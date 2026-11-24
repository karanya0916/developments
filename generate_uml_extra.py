import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('documentation/diagrams', exist_ok=True)

def generate_uml_class_diagram():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6, 6.6, "UML CLASS DIAGRAM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6, 6.25, "System Domain Entities, Attributes & Methods", fontsize=9.5, ha='center', color='#d97706')

    classes = [
        ("User", 1.8, 4.4, [
            "+ id: int", "+ username: str", "+ email: str", "+ role: str", "+ phone: str"
        ], [
            "+ authenticate()", "+ get_permissions()", "+ check_role()"
        ], "#dbeafe", "#1e40af"),
        ("Project", 5.8, 4.4, [
            "+ id: int", "+ code: str", "+ name: str", "+ budget: float", "+ actual_cost: float", "+ completion_pct: float"
        ], [
            "+ update_progress()", "+ compute_variance()", "+ get_tasks()"
        ], "#ffedd5", "#c2410c"),
        ("Task", 10.0, 4.4, [
            "+ id: int", "+ project_id: int", "+ title: str", "+ priority: str", "+ status: str"
        ], [
            "+ mark_completed()", "+ update_status()"
        ], "#f1f5f9", "#334155"),
        ("Material", 1.8, 1.8, [
            "+ id: int", "+ name: str", "+ brand: str", "+ current_stock: float", "+ min_threshold: float"
        ], [
            "+ record_movement()", "+ check_shortage()"
        ], "#dcfce7", "#15803d"),
        ("SiteDiaryEntry", 5.8, 1.8, [
            "+ id: int", "+ project_id: int", "+ entry_date: date", "+ daily_expense_total: float", "+ petty_expenses: list"
        ], [
            "+ tally_daily_expenses()", "+ sync_to_expenses()", "+ export_slip()"
        ], "#fef3c7", "#b45309"),
        ("Expense", 10.0, 1.8, [
            "+ id: int", "+ project_id: int", "+ category: str", "+ amount: float", "+ payment_mode: str"
        ], [
            "+ log_expense()", "+ audit_voucher()"
        ], "#fee2e2", "#b91c1c")
    ]

    for name, x, y, attrs, methods, bg, border in classes:
        box = patches.FancyBboxPatch((x - 1.4, y - 1.2), 2.8, 2.4, boxstyle="square,pad=0.05", fc=bg, ec=border, lw=1.5)
        ax.add_patch(box)
        # Class header
        ax.text(x, y + 0.9, f"<<Entity>>\n{name}", fontsize=8.5, fontweight='bold', ha='center', color=border)
        ax.plot([x - 1.4, x + 1.4], [y + 0.6, y + 0.6], color=border, lw=1)
        # Attributes
        ax.text(x - 1.3, y + 0.45, "\n".join(attrs), fontsize=7, va='top', color='#1e293b')
        ax.plot([x - 1.4, x + 1.4], [y - 0.4, y - 0.4], color=border, lw=1)
        # Methods
        ax.text(x - 1.3, y - 0.55, "\n".join(methods), fontsize=7, va='top', color='#1e293b')

    # Association connectors
    ax.plot([3.2, 4.4], [4.4, 4.4], color="#475569", lw=1.5)
    ax.text(3.8, 4.55, "1 .. *", fontsize=8, ha='center', color='#475569')

    ax.plot([7.2, 8.6], [4.4, 4.4], color="#475569", lw=1.5)
    ax.text(7.9, 4.55, "1 .. *", fontsize=8, ha='center', color='#475569')

    ax.plot([5.8, 5.8], [3.2, 3.0], color="#475569", lw=1.5)
    ax.text(5.95, 3.1, "1 .. *", fontsize=8, ha='left', color='#475569')

    ax.plot([7.2, 8.6], [1.8, 1.8], color="#475569", lw=1.5)
    ax.text(7.9, 1.95, "Syncs", fontsize=8, ha='center', color='#475569')

    plt.tight_layout()
    plt.savefig('documentation/diagrams/uml_class_diagram.png', bbox_inches='tight')
    plt.close()
    print("Generated: documentation/diagrams/uml_class_diagram.png")

def generate_uml_activity_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(5, 6.6, "UML ACTIVITY DIAGRAM: SITE DIARY & DAILY EXPENSES WORKFLOW", fontsize=12, fontweight='bold', ha='center', color='#0f172a')

    # Initial node
    init = patches.Circle((5, 6.0), 0.15, fc="#0f172a", ec="#0f172a")
    ax.add_patch(init)

    steps = [
        ("Site Engineer Logs in & Selects Active Project", 5, 5.2, "#f1f5f9"),
        ("Inspects Daily Structural Works (Columns/Rebar/Curing)", 5, 4.3, "#fff7ed"),
        ("Itemizes On-Site Petty Expenses (Tea/Tools/Fuel/Coolie)", 5, 3.4, "#fef3c7"),
        ("Attaches Photo Evidence & Digital Signature", 5, 2.5, "#dcfce7"),
        ("System Computes Daily Total & Syncs to Master Expenses", 5, 1.6, "#dbeafe"),
        ("Chief Builder (Sargu Sanju) Verifies & Archives Log", 5, 0.7, "#ede9fe")
    ]

    for text, x, y, bg in steps:
        box = patches.FancyBboxPatch((x - 3.0, y - 0.28), 6.0, 0.56, boxstyle="round,pad=0.08", fc=bg, ec="#475569", lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8.5, ha='center', va='center', fontweight='semibold', color='#0f172a')

    # Connecting vertical arrows
    for i in range(len(steps) - 1):
        ax.annotate('', xy=(5, steps[i+1][2] + 0.28), xytext=(5, steps[i][2] - 0.28), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.5))
    ax.annotate('', xy=(5, 5.48), xytext=(5, 5.85), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.5))

    # Final node
    final_outer = patches.Circle((5, 0.12), 0.18, fc="none", ec="#0f172a", lw=1.5)
    final_inner = patches.Circle((5, 0.12), 0.12, fc="#0f172a", ec="#0f172a")
    ax.add_patch(final_outer)
    ax.add_patch(final_inner)
    ax.annotate('', xy=(5, 0.3), xytext=(5, 0.42), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.5))

    plt.tight_layout()
    plt.savefig('documentation/diagrams/uml_activity_diagram.png', bbox_inches='tight')
    plt.close()
    print("Generated: documentation/diagrams/uml_activity_diagram.png")

def generate_uml_sequence_diagram():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(5.5, 6.6, "UML SEQUENCE DIAGRAM: AI COST ESTIMATION & BOQ TAKE-OFF", fontsize=12, fontweight='bold', ha='center', color='#0f172a')

    actors = [
        ("Homeowner / Client", 1.5),
        ("Web UI (Flask)", 4.0),
        ("Cost Estimation Engine", 6.8),
        ("Scikit-Learn ML Model", 9.5)
    ]

    for name, x in actors:
        box = patches.FancyBboxPatch((x - 1.1, 5.8), 2.2, 0.5, boxstyle="square,pad=0.05", fc="#f8fafc", ec="#0f172a", lw=1.5)
        ax.add_patch(box)
        ax.text(x, 6.05, name, fontsize=8, fontweight='bold', ha='center', color='#0f172a')
        ax.plot([x, x], [0.8, 5.8], color="#cbd5e1", lw=1.5, ls="--")

    # Messages
    msgs = [
        (1.5, 4.0, 5.2, "1. Submits Built-up Area, Floors & Quality Tier"),
        (4.0, 6.8, 4.5, "2. Invokes estimate_construction_cost()"),
        (6.8, 6.8, 3.8, "3. Computes CPWD / IS 456 BOQ Take-Off"),
        (6.8, 9.5, 3.1, "4. Queries RandomForestRegressor(features)"),
        (9.5, 6.8, 2.4, "5. Returns predicted cost components (R²=0.988)"),
        (6.8, 4.0, 1.7, "6. Aggregates BOQ items & ML variance bounds"),
        (4.0, 1.5, 1.0, "7. Renders interactive breakdown & recommended budget")
    ]

    for x1, x2, y, txt in msgs:
        if x1 < x2:
            ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5))
            ax.text((x1 + x2)/2, y + 0.12, txt, fontsize=7.5, ha='center', color="#0369a1", fontweight='semibold')
        elif x1 > x2:
            ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color="#10b981", lw=1.5, ls="--"))
            ax.text((x1 + x2)/2, y + 0.12, txt, fontsize=7.5, ha='center', color="#047857", fontweight='semibold')
        else:
            # Self invocation
            ax.plot([x1, x1 + 0.6, x1 + 0.6, x1], [y, y, y - 0.3, y - 0.3], color="#ea580c", lw=1.5)
            ax.text(x1 + 0.7, y - 0.15, txt, fontsize=7.5, va='center', color="#c2410c", fontweight='semibold')

    plt.tight_layout()
    plt.savefig('documentation/diagrams/uml_sequence_diagram.png', bbox_inches='tight')
    plt.close()
    print("Generated: documentation/diagrams/uml_sequence_diagram.png")

if __name__ == '__main__':
    generate_uml_class_diagram()
    generate_uml_activity_diagram()
    generate_uml_sequence_diagram()
