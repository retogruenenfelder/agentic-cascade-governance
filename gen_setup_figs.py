"""
Regenerate all figures — font sizes ~3× original for print legibility.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

NAVY="#003865"; GOLD="#C9A84C"; RED="#C0392B"; GRAY="#AAAAAA"; WHITE="#FFFFFF"
lam=1.0; d=8.0

# ── font size constants (change once here, applies everywhere) ────────────────
FS_SRC   = 20   # source / setup labels
FS_SCR   = 20   # "Screen" label
FS_SLIT  = 19   # narrow/wide slit labels
FS_DIST  = 20   # D₁/D₂/D₃ labels
FS_TITLE = 22   # panel titles
FS_AXIS  = 24   # x/y axis labels
FS_TICK  = 20   # tick numbers
FS_LEG   = 20   # legend
FS_ANNOT = 20   # annotations inside plot
FS_COL   = 24   # column/row headers (fig8)
FS_QUAD  = 19   # quadrant corner labels (fig8)
MS_SRC   = 16   # source marker size

def intensity(theta, a1, a2, d, offset=0.0):
    E1=np.sinc(a1*np.sin(theta)/lam); E2=np.sinc(a2*np.sin(theta)/lam)
    delta=2*np.pi/lam*d*np.sin(theta)+2*2*np.pi/lam*offset
    return np.clip(E1**2+E2**2+2*E1*E2*np.cos(delta),0,None)

def sy(theta,D): return D*np.tan(theta)


def draw_setup(ax, source_y=0, a1=2.0, a2=2.0,
               source_col=GOLD, label_source="Source\n(centred)",
               show_screen_dist=False, dist_label="D"):
    ax.set_xlim(-1, 11); ax.set_ylim(-7, 7)
    ax.set_facecolor(WHITE); ax.axis('off')
    barrier_x=5.0; gap_top=d/2; gap_bot=-d/2; wall_top=6.5; wall_bot=-6.5

    ax.add_patch(Rectangle((barrier_x-0.25,gap_top+a1/2),0.5,wall_top-(gap_top+a1/2),color=NAVY,zorder=3))
    ax.add_patch(Rectangle((barrier_x-0.25,gap_top-a1/2),0.5,1.5*a1 if a1<3 else 0.5,color=NAVY,zorder=3))
    ax.add_patch(Rectangle((barrier_x-0.25,gap_bot+a2/2),0.5,(gap_top-a1/2)-(gap_bot+a2/2),color=NAVY,zorder=3))
    ax.add_patch(Rectangle((barrier_x-0.25,wall_bot),0.5,(gap_bot-a2/2)-wall_bot,color=NAVY,zorder=3))
    ax.add_patch(Rectangle((barrier_x-0.3,gap_top-a1/2),0.6,a1,color=WHITE,zorder=4))
    ax.add_patch(Rectangle((barrier_x-0.3,gap_bot-a2/2),0.6,a2,color=WHITE,zorder=4))

    for gap,a in [(gap_top,a1),(gap_bot,a2)]:
        ax.annotate('',xy=(barrier_x+0.5,gap+a/2),xytext=(barrier_x+0.5,gap-a/2),
                    arrowprops=dict(arrowstyle='<->',color=NAVY,lw=1.4))

    ax.plot(1.0,source_y,'o',color=source_col,ms=MS_SRC,zorder=6)
    ax.text(1.0,source_y+0.7,label_source,ha='center',va='bottom',
            fontsize=FS_SRC,color=source_col,fontweight='bold')

    for gap in [gap_top,gap_bot]:
        ax.annotate('',xy=(barrier_x-0.25,gap),xytext=(1.0,source_y),
                    arrowprops=dict(arrowstyle='->',color=source_col,lw=2.0,alpha=0.8))

    screen_x=9.5
    ax.plot([screen_x,screen_x],[-6,6],color=GRAY,lw=2.5,zorder=2)
    ax.text(screen_x+0.3,5.5,'Screen',ha='left',va='top',fontsize=FS_SCR,color=GRAY)

    if show_screen_dist:
        ax.annotate('',xy=(screen_x,-5.5),xytext=(barrier_x,-5.5),
                    arrowprops=dict(arrowstyle='<->',color=GRAY,lw=1.4))
        ax.text((barrier_x+screen_x)/2,-6.3,dist_label,ha='center',
                fontsize=FS_SRC,color=GRAY,style='italic')

    for gap in [gap_top,gap_bot]:
        for r in [1.5,2.8,4.0]:
            theta_arc=np.linspace(-np.pi/2,np.pi/2,80)
            xarc=barrier_x+r*np.cos(theta_arc); yarc=gap+r*np.sin(theta_arc)
            mask=(xarc<screen_x)&(yarc>-6.5)&(yarc<6.5)
            if mask.sum()>2:
                ax.plot(xarc[mask],yarc[mask],color=NAVY,lw=1.0,ls='--',alpha=0.35,zorder=1)


# ── FIG 1 ─────────────────────────────────────────────────────────────────────
def fig1():
    th=np.linspace(-0.12,0.12,4000); D=200
    I=intensity(th,2,2,d,0); y=sy(th,D)
    fig,axes=plt.subplots(1,2,figsize=(14,7.0),gridspec_kw={"width_ratios":[1,1.4]})
    fig.patch.set_facecolor(WHITE)
    draw_setup(axes[0],source_y=0,a1=2.0,a2=2.0,source_col=GOLD,label_source="Source\n(centred)")
    axes[0].set_title("Experimental setup",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax=axes[1]; ax.set_facecolor(WHITE)
    ax.fill_betweenx(y,0,I/I.max(),color=NAVY,alpha=0.85)
    ax.axhline(0,color=GOLD,lw=1.5,ls='--',alpha=0.7)
    ax.set_xlabel("Relative intensity",fontsize=FS_AXIS,color=NAVY)
    ax.set_ylabel("Position on screen",fontsize=FS_AXIS,color=NAVY)
    ax.set_title("Interference pattern",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax.tick_params(colors=NAVY,labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig1.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig1")


# ── FIG 2 ─────────────────────────────────────────────────────────────────────
def fig2():
    th=np.linspace(-0.15,0.15,4000); D=200
    shift=10.0
    I=intensity(th,2,2,d,0)
    y_c=sy(th,D); y_o=sy(th,D)+shift
    fig,axes=plt.subplots(1,2,figsize=(14,7.0),gridspec_kw={"width_ratios":[1,1.4]})
    fig.patch.set_facecolor(WHITE)
    draw_setup(axes[0],source_y=2.2,a1=2.0,a2=2.0,source_col=RED,label_source="Source\n(off-centre)")
    axes[0].set_title("Experimental setup",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax=axes[1]; ax.set_facecolor(WHITE)
    ax.plot(I/I.max(),y_c,color=NAVY,lw=2.5,ls='--',label='Centred (reference)')
    ax.fill_betweenx(y_o,0,I/I.max(),color=RED,alpha=0.75,label='Off-centre source')
    ax.annotate('',xy=(0.5,shift),xytext=(0.5,0),
                arrowprops=dict(arrowstyle='<->',color=RED,lw=2.5))
    ax.text(0.55,shift/2,'Systematic\nbias',fontsize=FS_ANNOT,color=RED,va='center')
    ax.legend(fontsize=FS_LEG,framealpha=0.3)
    ax.set_xlabel("Relative intensity",fontsize=FS_AXIS,color=NAVY)
    ax.set_ylabel("Position on screen",fontsize=FS_AXIS,color=NAVY)
    ax.set_title("Interference pattern",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax.tick_params(colors=NAVY,labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig2.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig2")


# ── FIG 3 ─────────────────────────────────────────────────────────────────────
def fig3():
    th=np.linspace(-0.18,0.18,4000); D=200
    fig,axes=plt.subplots(1,2,figsize=(15,7.0),gridspec_kw={"width_ratios":[1,1.4]})
    fig.patch.set_facecolor(WHITE)
    ax_s=axes[0]; ax_s.set_facecolor(WHITE); ax_s.axis('off')
    ax_s.set_xlim(0,16); ax_s.set_ylim(-8,8)
    # Side by side: narrow (left) and wide (right), well separated
    for bx,sx,a,col,lbl in [(4.5,1.5,1.0,RED,"Narrow\n(small scope)"),
                              (11.5,8.5,3.5,NAVY,"Wide\n(large scope)")]:
        wall_h=6.5
        # Barrier walls above and below slit
        ax_s.add_patch(Rectangle((bx-0.2, a/2),    0.4, wall_h-a/2, color=col,zorder=3,alpha=0.8))
        ax_s.add_patch(Rectangle((bx-0.2,-wall_h),  0.4, wall_h-a/2, color=col,zorder=3,alpha=0.8))
        # Slit gap
        ax_s.add_patch(Rectangle((bx-0.25,-a/2),0.5,a,color=WHITE,zorder=4))
        # Width arrow on right side of barrier
        ax_s.annotate('',xy=(bx+0.7,a/2),xytext=(bx+0.7,-a/2),
                      arrowprops=dict(arrowstyle='<->',color=col,lw=1.8))
        # Source dot
        ax_s.plot(sx,0,'o',color=GOLD,ms=MS_SRC,zorder=6)
        # Arrow source → slit centre
        ax_s.annotate('',xy=(bx-0.25,0),xytext=(sx+0.35,0),
                      arrowprops=dict(arrowstyle='->',color=GOLD,lw=2.0))
        # Label below barrier, with clearance
        ax_s.text(bx,-wall_h-0.8,lbl,ha='center',va='top',
                  fontsize=FS_SLIT,color=col,fontweight='bold')
    ax_s.set_title("Experimental setup",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax=axes[1]; ax.set_facecolor(WHITE)
    for a,col,lbl in [(1.0,RED,"Narrow slit — wide, uncertain output"),
                      (3.5,NAVY,"Wide slit — narrow, precise output")]:
        I=np.sinc(a*np.sin(th)/lam)**2
        ax.plot(I/I.max(),sy(th,D),color=col,lw=2.8,label=lbl)
    ax.axhline(0,color=GOLD,lw=1.5,ls='--',alpha=0.5)
    ax.set_xlabel("Relative intensity",fontsize=FS_AXIS,color=NAVY)
    ax.set_ylabel("Position on screen",fontsize=FS_AXIS,color=NAVY)
    ax.set_title("Single-slit diffraction pattern",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax.legend(fontsize=FS_LEG,framealpha=0.3)
    ax.tick_params(colors=NAVY,labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig3.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig3")


# ── FIG 4 ─────────────────────────────────────────────────────────────────────
def fig4():
    """Show fringe visibility collapse as slit asymmetry increases.
    Three cases: equal, moderate, extreme. Line plots so minima are visible."""
    th=np.linspace(-0.18,0.18,6000); D=200; y=sy(th,D)

    cases = [
        (2.0, 2.0, NAVY, 'solid',  2.8, "Equal  (a₁ = a₂ = 2)  —  deep fringes, minima = 0"),
        (1.0, 3.5, GOLD, 'dashed', 2.8, "Moderate  (a₁=1, a₂=3.5)  —  reduced visibility"),
        (0.1, 8.0, RED,  'solid',  2.8, "Extreme  (a₁=0.1, a₂=8)  —  wide slit dominates, fringes collapse"),
    ]
    # Normalise all to equal-slit maximum
    norm = intensity(th,2,2,d,0).max()

    fig,axes=plt.subplots(1,2,figsize=(15,7.0),gridspec_kw={"width_ratios":[1,1.4]})
    fig.patch.set_facecolor(WHITE)

    # ── Left panel: show extreme case geometry ──
    ax_s=axes[0]; ax_s.set_facecolor(WHITE); ax_s.axis('off')
    ax_s.set_xlim(-1,11); ax_s.set_ylim(-9,8)
    bx=5.0; a_top=0.4; a_bot=4.5   # extreme but with visible wall at bottom
    gt=d/2; gb=-d/2; wt=7.5; wb=-8.5
    # Top wall
    ax_s.add_patch(Rectangle((bx-0.25,gt+a_top/2),0.5,wt-(gt+a_top/2),color=NAVY,zorder=3))
    # Between slits
    ax_s.add_patch(Rectangle((bx-0.25,gb+a_bot/2),0.5,(gt-a_top/2)-(gb+a_bot/2),color=NAVY,zorder=3))
    # Bottom wall — now has 1.25 units of visible wall
    ax_s.add_patch(Rectangle((bx-0.25,wb),0.5,(gb-a_bot/2)-wb,color=NAVY,zorder=3))
    # Slit gaps
    ax_s.add_patch(Rectangle((bx-0.3,gt-a_top/2),0.6,a_top,color=WHITE,zorder=4))
    ax_s.add_patch(Rectangle((bx-0.3,gb-a_bot/2),0.6,a_bot,color=WHITE,zorder=4))
    # Width arrows
    ax_s.annotate('',xy=(bx+0.7,gt+a_top/2),xytext=(bx+0.7,gt-a_top/2),
                  arrowprops=dict(arrowstyle='<->',color=RED,lw=1.6))
    ax_s.text(bx+1.0,gt,'very\nnarrow',ha='left',fontsize=FS_SLIT-2,color=RED)
    ax_s.annotate('',xy=(bx+0.7,gb+a_bot/2),xytext=(bx+0.7,gb-a_bot/2),
                  arrowprops=dict(arrowstyle='<->',color=NAVY,lw=1.6))
    ax_s.text(bx+1.0,gb,'very\nwide',ha='left',fontsize=FS_SLIT-2,color=NAVY)
    # Source and rays
    ax_s.plot(1.0,0,'o',color=GOLD,ms=MS_SRC,zorder=6)
    ax_s.text(1.0,0.9,'Source\n(centred)',ha='center',fontsize=FS_SRC,color=GOLD,fontweight='bold')
    for gap in [gt,gb]:
        ax_s.annotate('',xy=(bx-0.25,gap),xytext=(1.0,0),
                      arrowprops=dict(arrowstyle='->',color=GOLD,lw=2.0,alpha=0.8))
    ax_s.plot([9.5,9.5],[-7,7],color=GRAY,lw=2.5)
    ax_s.text(9.7,6.5,'Screen',fontsize=FS_SCR,color=GRAY)
    axes[0].set_title("Experimental setup\n(extreme case shown)",fontsize=FS_TITLE,color=NAVY,pad=8)

    # ── Right panel: three line plots ──
    ax=axes[1]; ax.set_facecolor(WHITE)
    for a1,a2,col,ls,lw,lbl in cases:
        I=intensity(th,a1,a2,d,0)
        ax.plot(I/norm,y,color=col,lw=lw,ls=ls,label=lbl)
    ax.axhline(0,color=GRAY,lw=1.5,ls='--')
    # Annotate fringe collapse — point to outer region (y≈28) where red is flat
    I_ext=intensity(th,0.1,8.0,d,0)
    # Find point near y=28 where blue has a clear lobe but red is flat
    target_y=28.0
    outer_idx=int(np.argmin(np.abs(y-target_y)))
    ax.annotate('Outer fringes\ncollapsed here',
                xy=(I_ext[outer_idx]/norm, y[outer_idx]),
                xytext=(0.45, y[outer_idx]+5),
                fontsize=FS_ANNOT-2,color=RED,
                arrowprops=dict(arrowstyle='->',color=RED,lw=1.8))
    # Note: central lobe unchanged — physics + governance insight
    ax.text(0.98, 0.50,
            "Central lobe identical\nfor all slit ratios\n(sinc(0) = 1 always).\n\n"
            "An observer at y = 0\nsees no problem —\nthe failure is only\n"
            "visible in the outer\nlobes, away from\nthe peak output.",
            transform=ax.transAxes, fontsize=FS_ANNOT-5, color=NAVY,
            va='center', ha='right', style='italic',
            bbox=dict(boxstyle='round,pad=0.4',fc=WHITE,ec=NAVY,alpha=0.85))
    ax.set_xlabel("Relative intensity",fontsize=FS_AXIS,color=NAVY)
    ax.set_ylabel("Position on screen",fontsize=FS_AXIS,color=NAVY)
    ax.set_title("Fringe visibility vs. slit asymmetry",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax.legend(fontsize=FS_LEG-2,framealpha=0.3,
              loc='upper center',bbox_to_anchor=(0.5,-0.18),ncol=1)
    ax.tick_params(colors=NAVY,labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig4.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig4")


# ── FIG 5 (was fig6) ──────────────────────────────────────────────────────────
def fig5():
    fig,axes=plt.subplots(1,2,figsize=(16,7.5),gridspec_kw={"width_ratios":[1.2,1.4]})
    fig.patch.set_facecolor(WHITE)
    ax_s=axes[0]; ax_s.set_facecolor(WHITE); ax_s.axis('off')
    ax_s.set_xlim(-1,15); ax_s.set_ylim(-9,7)
    bx=3.0
    ax_s.add_patch(Rectangle((bx-0.25,d/2+1.0),0.5,5.5-(d/2+1.0),color=NAVY,zorder=3))
    ax_s.add_patch(Rectangle((bx-0.25,-d/2+1.0),0.5,(d/2-1.0)-(-d/2+1.0),color=NAVY,zorder=3))
    ax_s.add_patch(Rectangle((bx-0.25,-5.5),0.5,(-d/2-1.0)+5.5,color=NAVY,zorder=3))
    ax_s.add_patch(Rectangle((bx-0.3,d/2-1.0),0.6,2.0,color=WHITE,zorder=4))
    ax_s.add_patch(Rectangle((bx-0.3,-d/2-1.0),0.6,2.0,color=WHITE,zorder=4))
    ax_s.plot(0.5,0,'o',color=GOLD,ms=MS_SRC,zorder=6)
    ax_s.text(0.5,0.9,'Source\n(centred)',ha='center',fontsize=FS_SRC,color=GOLD)
    # stagger role labels vertically to avoid collision
    for xscr,col,dlbl,rlbl,y_lbl in [(6.5,NAVY,"D₁","Internal\nrisk team",-6.2),
                                      (10,GOLD,"D₂","Board\nreview",-7.2),
                                      (13.5,RED,"D₃","Regulatory\nexamination",-6.2)]:
        ax_s.plot([xscr,xscr],[-5.5,5.5],color=col,lw=2.2,alpha=0.85)
        ax_s.text(xscr,6.2,dlbl,ha='center',fontsize=FS_DIST,color=col,fontweight='bold')
        ax_s.text(xscr,y_lbl,rlbl,ha='center',fontsize=FS_DIST-1,color=col,style='italic',va='top')
        ax_s.annotate('',xy=(xscr,-5.8),xytext=(bx,-5.8),
                      arrowprops=dict(arrowstyle='<->',color=col,lw=1.2,alpha=0.7))
    axes[0].set_title("Setup: three screen distances",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax=axes[1]; ax.set_facecolor(WHITE)
    for dist,col,lbl in [(100,NAVY,"D₁ — Internal risk team"),
                         (200,GOLD,"D₂ — Board review"),
                         (400,RED,"D₃ — Regulatory examination")]:
        th=np.linspace(-0.15,0.15,4000); I=intensity(th,2,2,d,0); y=sy(th,dist)
        ax.plot(I/I.max(),y,color=col,lw=2.8,label=lbl)
    ax.axhline(0,color=GRAY,lw=1.5,ls='--')
    ax.set_xlabel("Relative intensity",fontsize=FS_AXIS,color=NAVY)
    ax.set_ylabel("Position on screen",fontsize=FS_AXIS,color=NAVY)
    ax.set_title("Pattern at each screen distance",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax.legend(fontsize=FS_LEG,framealpha=0.3)
    ax.tick_params(colors=NAVY,labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig5.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig5")


# ── FIG 6 (was fig7) ─────────────────────────────────────────────────────────
def fig6():
    fig,axes=plt.subplots(1,2,figsize=(15,7.2),gridspec_kw={"width_ratios":[1,1.4]})
    fig.patch.set_facecolor(WHITE)
    ax_s=axes[0]; ax_s.set_facecolor(WHITE); ax_s.axis('off')
    ax_s.set_xlim(-1,13); ax_s.set_ylim(-9.5,7.5)
    bx=3.0; a_top=0.8; a_bot=4.0
    wt=6.5; wb=-8.5   # visible wall boundaries
    # Top wall
    ax_s.add_patch(Rectangle((bx-0.25,d/2+a_top/2),0.5,wt-(d/2+a_top/2),color=NAVY,zorder=3))
    # Between slits
    ax_s.add_patch(Rectangle((bx-0.25,-d/2+a_bot/2),0.5,(d/2-a_top/2)-(-d/2+a_bot/2),color=NAVY,zorder=3))
    # Bottom wall — now clearly visible
    ax_s.add_patch(Rectangle((bx-0.25,wb),0.5,(-d/2-a_bot/2)-wb,color=NAVY,zorder=3))
    # Slit gaps (white)
    ax_s.add_patch(Rectangle((bx-0.3,d/2-a_top/2),0.6,a_top,color=WHITE,zorder=4))
    ax_s.add_patch(Rectangle((bx-0.3,-d/2-a_bot/2),0.6,a_bot,color=WHITE,zorder=4))
    ax_s.plot(0.5,2.2,'o',color=RED,ms=MS_SRC,zorder=6)
    ax_s.text(0.5,3.1,'Source\n(off-centre)',ha='center',fontsize=FS_SRC,color=RED)
    for xscr,col,lbl in [(6,NAVY,"D₁"),(8.5,GOLD,"D₂"),(11,RED,"D₃")]:
        ax_s.plot([xscr,xscr],[-8.0,6.5],color=col,lw=2.2,alpha=0.85)
        ax_s.text(xscr,7.0,lbl,ha='center',fontsize=FS_DIST,color=col,fontweight='bold')
    ax_s.text(5.0,-9.0,"Slits: narrow (top) + wide (bottom)",
              ha='center',fontsize=FS_SLIT,color=NAVY,style='italic')
    axes[0].set_title("Setup: off-centre source + unequal slits",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax=axes[1]; ax.set_facecolor(WHITE)
    for dist,col,lbl in [(100,NAVY,"D₁ — Internal"),
                         (200,GOLD,"D₂ — Board"),
                         (400,RED,"D₃ — Regulator")]:
        th=np.linspace(-0.25,0.25,6000); I=intensity(th,0.8,4.0,d,1.8); y=sy(th,dist)
        ax.plot(I/I.max(),y,color=col,lw=2.8,label=lbl)
    ax.axhline(0,color=GRAY,lw=1.5,ls='--')
    ax.set_xlabel("Relative intensity",fontsize=FS_AXIS,color=NAVY)
    ax.set_ylabel("Position on screen",fontsize=FS_AXIS,color=NAVY)
    ax.set_title("Pattern at each screen distance",fontsize=FS_TITLE,color=NAVY,pad=8)
    ax.legend(fontsize=FS_LEG,framealpha=0.3)
    ax.tick_params(colors=NAVY,labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig6.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig6")


# ── FIG 7 (was fig8) ─────────────────────────────────────────────────────────
def fig7():
    """2×2 governance matrix. Non-MECE cases shown as physically shifted patterns."""
    th=np.linspace(-0.20,0.20,4000); D=200; shift=20.0  # shift increased for visual clarity

    # (a1, a2, y_shift, col, corner_lbl, verdict, bcol)
    # Unequal scope: extreme asymmetry (0.5:5.5) to make fringe collapse visible
    configs=[
        (2.0,2.0,0.0,  NAVY,"MECE data\nEqual scope",   "Distance-invariant\n✓ All observers agree",NAVY),
        (0.5,5.5,0.0,  GOLD,"MECE data\nUnequal scope",  "One agent dominates\n— asymmetric output",GOLD),
        (2.0,2.0,shift,GOLD,"Non-MECE data\nEqual scope","Systematic source bias\n— pattern shifted",GOLD),
        (0.5,5.5,shift,RED, "Non-MECE data\nUnequal scope","Compounded failure\n✗ No observer agrees",RED),
    ]
    fig,axes=plt.subplots(2,2,figsize=(15,12))
    fig.patch.set_facecolor(WHITE)
    for (r,c),(a1,a2,ys,col,clbl,verdict,bcol) in zip([(0,0),(0,1),(1,0),(1,1)],configs):
        ax=axes[r][c]; ax.set_facecolor(WHITE)
        I=intensity(th,a1,a2,d,0); y=sy(th,D)+ys
        ax.fill_betweenx(y,0,I/I.max(),color=col,alpha=0.80)
        if ys>0:  # show reference outline for non-MECE
            ax.plot(I/I.max(),sy(th,D),color=NAVY,lw=1.8,ls='--',alpha=0.4)
        ax.axhline(0,color=GRAY,lw=1.2,ls='--')
        ax.set_xlabel("Relative intensity",fontsize=FS_AXIS-2,color=NAVY)
        ax.set_ylabel("Position on screen",fontsize=FS_AXIS-2,color=NAVY)
        ax.tick_params(colors=NAVY,labelsize=FS_TICK-2)
        for sp in ax.spines.values():
            sp.set_color(bcol); sp.set_linewidth(3.0 if bcol==NAVY else 1.8)
        ax.text(0.03,0.97,clbl,transform=ax.transAxes,fontsize=FS_QUAD,color=col,
                fontweight='bold',va='top',ha='left',
                bbox=dict(boxstyle='round,pad=0.3',fc=WHITE,ec=col,alpha=0.85))
        ax.text(0.97,0.03,verdict,transform=ax.transAxes,fontsize=FS_QUAD,
                color=bcol,va='bottom',ha='right',style='italic')
    for ci,lbl in enumerate(["Equal agent scope  (a₁ = a₂)","Unequal agent scope  (a₁ ≠ a₂)"]):
        axes[0][ci].set_title(lbl,fontsize=FS_COL,color=NAVY,fontweight='bold',pad=12)
    for ri,lbl in enumerate(["MECE data","Non-MECE data"]):
        axes[ri][0].set_ylabel(f"{lbl}\n\nPosition on screen",fontsize=FS_AXIS-2,color=NAVY)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig7.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig7")


# ── FIG 8 (was fig9) ─────────────────────────────────────────────────────────
def fig8():
    """The Fresnel Excuse: compensatory tweaks that pass the team's governance
    check (D=200) but fail at the regulator's screen (D=600).
    A governance tolerance band (same ABSOLUTE range on both panels) shows the divergence.
    - Data-only tweak (offset=0.12): central fringe at y≈−6 at D=200 (within band),
      same drift → y≈−18 at D=600 (outside band).
    - Agent-only tweak (0.5:5.5 scope imbalance): fringe-visibility collapse at both
      distances, but fine structure at D=200 lets the team argue it away; at D=600
      the flat envelope is unmistakable.
    """
    configs = [
        (2.0, 2.0, 0.00, NAVY, "Ground truth  (MECE + equal scope)"),
        (2.0, 2.0, 0.12, GOLD, "Fresnel Excuse: data only  (source drift)"),
        (0.5, 5.5, 0.00, RED,  "Fresnel Excuse: agents only  (scope imbalance)"),
        (0.5, 5.5, 0.12, GRAY, "Fresnel Excuse: both compounded"),
    ]
    tol  = 7.0    # governance tolerance band (absolute units)
    ylim = 55.0   # fixed on BOTH panels — full extent of team's screen (D=200)
                  # at D=600 fringe spacing = λD/d = 75 units → fringes lie outside
                  # window; only the central envelope is visible to the regulator
    th = np.linspace(-0.25, 0.25, 6000)
    fig, axes = plt.subplots(1, 2, figsize=(16, 8.0))
    fig.patch.set_facecolor(WHITE)
    handles = []
    for ax_i, (D_use, title, tcol) in enumerate(
            [(200, "Team's screen", NAVY),
             (600, "Regulator's screen", RED)]):
        ax = axes[ax_i]; ax.set_facecolor(WHITE)
        y = D_use * np.tan(th)
        # Tolerance band — same absolute range on both panels
        ax.axhspan(-tol, tol, color=GOLD, alpha=0.09, zorder=0)
        ax.axhline( tol, color=GOLD, lw=1.3, ls=':', alpha=0.8, zorder=1)
        ax.axhline(-tol, color=GOLD, lw=1.3, ls=':', alpha=0.8, zorder=1)
        for a1, a2, off, col, lbl in configs:
            I = intensity(th, a1, a2, d, off)
            h, = ax.plot(I/I.max(), y, color=col, lw=2.8, label=lbl)
            if ax_i == 0: handles.append(h)
        ax.axhline(0, color=GRAY, lw=1.2, ls='--')
        ax.set_ylim(-ylim, ylim)
        ax.set_xlabel("Relative intensity", fontsize=FS_AXIS, color=NAVY)
        ax.set_ylabel("Screen position (absolute units)", fontsize=FS_AXIS, color=NAVY)
        ax.set_title(title, fontsize=FS_TITLE, color=tcol, fontweight='bold')
        ax.tick_params(colors=NAVY, labelsize=FS_TICK)
        for sp in ax.spines.values(): sp.set_color(NAVY)
        if ax_i == 0:
            ax.text(0.50, 0.03,
                    'All configurations within tolerance band\n— team declares all pass',
                    transform=ax.transAxes, fontsize=FS_ANNOT-5, color=NAVY,
                    ha='center', va='bottom', style='italic',
                    bbox=dict(boxstyle='round,pad=0.3', fc=WHITE, ec=NAVY, alpha=0.85))
        else:
            ax.text(0.50, 0.03,
                    'Data tweak: outside band  ·  Fringe spacing > window: regulator sees only envelope',
                    transform=ax.transAxes, fontsize=FS_ANNOT-5, color=RED,
                    ha='center', va='bottom', style='italic',
                    bbox=dict(boxstyle='round,pad=0.3', fc=WHITE, ec=RED, alpha=0.85))
    fig.legend(handles=handles, fontsize=FS_LEG, framealpha=0.3,
               loc='lower center', bbox_to_anchor=(0.5, 0.0), ncol=2)
    plt.tight_layout(rect=[0, 0.12, 1, 1])
    plt.savefig(f"{OUT}/fig8.png", dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(); print("fig8")


# ── FIG 9 (was fig10) ────────────────────────────────────────────────────────
def fig9():
    fig=plt.figure(figsize=(18,8.5))
    fig.patch.set_facecolor(WHITE)
    ax_s=fig.add_axes([0.01,0.08,0.22,0.82])
    ax_s.set_facecolor(WHITE); ax_s.axis('off')
    ax_s.set_xlim(-1,11); ax_s.set_ylim(-7,7)
    bx=3.5; a=2.0
    ax_s.add_patch(Rectangle((bx-0.25,d/2+a/2),0.5,5.5-(d/2+a/2),color=NAVY,zorder=3))
    ax_s.add_patch(Rectangle((bx-0.25,-d/2+a/2),0.5,(d/2-a/2)-(-d/2+a/2),color=NAVY,zorder=3))
    ax_s.add_patch(Rectangle((bx-0.25,-5.5),0.5,(-d/2-a/2)+5.5,color=NAVY,zorder=3))
    ax_s.add_patch(Rectangle((bx-0.3,d/2-a/2),0.6,a,color=WHITE,zorder=4))
    ax_s.add_patch(Rectangle((bx-0.3,-d/2-a/2),0.6,a,color=WHITE,zorder=4))
    ax_s.plot(0.5,0,'o',color=GOLD,ms=MS_SRC,zorder=6)
    ax_s.text(0.5,0.9,'Source\n(centred)',ha='center',fontsize=FS_SRC,color=GOLD,fontweight='bold')
    for gap in [d/2,-d/2]:
        ax_s.annotate('',xy=(bx-0.25,gap),xytext=(0.5,0),
                      arrowprops=dict(arrowstyle='->',color=GOLD,lw=1.8,alpha=0.8))
    for xscr,col,lbl in [(5.5,NAVY,"D₁"),(7.5,GOLD,"D₂"),(9.5,RED,"D₃")]:
        ax_s.plot([xscr,xscr],[-5.5,5.5],color=col,lw=2.0,alpha=0.85)
        ax_s.text(xscr,6.2,lbl,ha='center',fontsize=FS_DIST,color=col,fontweight='bold')
    ax_s.text(5.0,-6.5,"Equal slits (a₁ = a₂)",ha='center',fontsize=FS_SRC,color=NAVY,style='italic')
    ax_s.set_title("Setup",fontsize=FS_TITLE,color=NAVY,pad=8)
    for i,(dist,col,lbl) in enumerate([(100,NAVY,"Internal risk team"),
                                        (200,GOLD,"Board review"),
                                        (400,RED,"Regulatory exam")]):
        ax=fig.add_axes([0.26+i*0.24,0.08,0.22,0.82])
        ax.set_facecolor(WHITE)
        th=np.linspace(-0.15,0.15,4000); I=intensity(th,2,2,d,0); y=dist*np.tan(th)
        ax.fill_betweenx(y,0,I/I.max(),color=col,alpha=0.82)
        ax.axhline(0,color=GRAY,lw=1.2,ls='--')
        ax.set_title(lbl,fontsize=FS_TITLE,color=col,fontweight='bold')
        ax.set_xlabel("Intensity",fontsize=FS_AXIS-2,color=NAVY)
        ax.set_ylabel("Screen position",fontsize=FS_AXIS-2,color=NAVY)
        ax.tick_params(colors=NAVY,labelsize=FS_TICK-2)
        for sp in ax.spines.values(): sp.set_color(NAVY)
        ax.text(0.5,0.03,f"Scale ∝ D={dist}",ha='center',transform=ax.transAxes,
                fontsize=FS_ANNOT,color=col,style='italic')
    plt.savefig(f"{OUT}/fig9.png",dpi=200,bbox_inches='tight',facecolor=WHITE)
    plt.close(); print("fig9")



# ── FIG 10 ────────────────────────────────────────────────────────────────────
def fig10():
    """Cascade Architecture: Huygens handoff from Layer 1 to Layer 2.
    Three observer screens at increasing distances: Risk team (Fresnel),
    Board (intermediate), Regulator (Fraunhofer)."""
    fig, ax = plt.subplots(figsize=(22, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.axis('off')
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 10)

    CY   = 5.0   # vertical centre
    SG   = 1.5   # half-distance between slit centres
    SW   = 0.75  # slit width (half)

    def mini_barrier(bx):
        tc = CY + SG; bc = CY - SG
        wt = CY + SG*2.1; wb = CY - SG*2.1
        ax.add_patch(Rectangle((bx-.18, tc+SW), .36, wt-(tc+SW), color=NAVY, zorder=3))
        ax.add_patch(Rectangle((bx-.18, bc+SW), .36, (tc-SW)-(bc+SW), color=NAVY, zorder=3))
        ax.add_patch(Rectangle((bx-.18, wb),     .36, (bc-SW)-wb,     color=NAVY, zorder=3))
        ax.add_patch(Rectangle((bx-.22, tc-SW),  .44, SW*2, color=WHITE, zorder=4))
        ax.add_patch(Rectangle((bx-.22, bc-SW),  .44, SW*2, color=WHITE, zorder=4))
        return tc, bc

    def arcs(bx, tc, bc, xmax, col, alpha=0.35):
        for sy in [tc, bc]:
            for r in [0.6, 1.3, 2.0]:
                th = np.linspace(-np.pi/2, np.pi/2, 80)
                xa = bx + r*np.cos(th); ya = sy + r*np.sin(th)
                m = (xa < xmax) & (ya > 0.4) & (ya < 9.5)
                if m.sum() > 2:
                    ax.plot(xa[m], ya[m], color=col, lw=1.0, ls='--', alpha=alpha, zorder=1)

    def fringes(sx, col, n=7, spacing=0.85):
        for i in range(n):
            fy = CY + (i - n//2)*spacing
            alpha = max(0.18, 0.92 - abs(i - n//2)*0.14)
            ms    = max(4,    15   - abs(i - n//2)*2.5)
            ax.plot(sx, fy, 'o', color=col, ms=ms, alpha=alpha, zorder=7)

    # ── CRO meta-plane banner ─────────────────────────────────────────────────
    ax.add_patch(Rectangle((0.2, 9.05), 21.5, 0.75,
                            facecolor=NAVY, alpha=0.07, edgecolor=NAVY, lw=1.2))
    ax.text(11.0, 9.43,
            'CRO: certifies structural conditions at every layer and at every transition',
            ha='center', va='center', fontsize=FS_ANNOT-1, color=NAVY, fontweight='bold')

    # ── LAYER 1 ───────────────────────────────────────────────────────────────
    ax.add_patch(Rectangle((0.2, 0.25), 6.9, 8.75,
                            facecolor=NAVY, alpha=0.03, edgecolor=NAVY, lw=1.0, ls='--'))
    ax.text(3.55, 8.75, 'LAYER 1', ha='center', va='top',
            fontsize=FS_TITLE-1, color=NAVY, fontweight='bold')

    ax.plot(1.0, CY, 'o', color=GOLD, ms=18, zorder=6)
    ax.text(1.0, CY+1.0, 'Data source\n(CDO)', ha='center', va='bottom',
            fontsize=FS_SRC-3, color=GOLD, fontweight='bold')

    bx1 = 3.6
    tc1, bc1 = mini_barrier(bx1)
    ax.text(bx1+0.35, 1.0, 'Layer 1\nAgents', ha='left', fontsize=FS_SRC-4, color=NAVY)

    for sc in [tc1, bc1]:
        ax.annotate('', xy=(bx1-.2, sc), xytext=(1.0, CY),
                    arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.0, alpha=0.65))

    sx1 = 5.9
    arcs(bx1, tc1, bc1, sx1+0.1, NAVY)
    ax.plot([sx1, sx1], [0.6, 8.8], color=NAVY, lw=2.8, zorder=5)
    ax.text(sx1+0.2, 1.0, 'Screen 1', ha='left', fontsize=FS_SCR-3, color=NAVY)
    fringes(sx1, NAVY)

    # ── HANDOFF ─── fan arrows from 3 central fringes → L2 source cluster ────
    for fy, ty in [(CY, CY), (CY+0.75, CY+0.75), (CY-0.75, CY-0.75)]:
        ax.annotate('', xy=(9.2, ty), xytext=(sx1+0.12, fy),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.0, alpha=0.65))
    ax.text(7.45, CY+1.15, "Huygens' principle:",
            ha='center', fontsize=FS_ANNOT-3, color=NAVY, fontweight='bold')
    ax.text(7.45, CY+0.45, "each bright fringe",
            ha='center', fontsize=FS_ANNOT-4, color=NAVY, style='italic')
    ax.text(7.45, CY-0.25, "= new secondary emitter",
            ha='center', fontsize=FS_ANNOT-4, color=NAVY, style='italic')

    # ── LAYER 2 ───────────────────────────────────────────────────────────────
    ax.add_patch(Rectangle((8.9, 0.25), 12.8, 8.75,
                            facecolor=RED, alpha=0.03, edgecolor=RED, lw=1.0, ls='--'))
    ax.text(12.0, 8.75, 'LAYER 2', ha='center', va='top',
            fontsize=FS_TITLE-1, color=RED, fontweight='bold')

    # Inherited fringes (secondary emitters from L1)
    for i in range(5):
        fy    = CY + (i-2)*0.75
        alpha = max(0.20, 0.85 - abs(i-2)*0.15)
        ms    = max(5, 13  - abs(i-2)*2.5)
        ax.plot(9.4, fy, 'o', color=NAVY, ms=ms, alpha=alpha, zorder=6)
    # Own data
    ax.plot(9.4, 1.2, 'o', color=GOLD, ms=14, zorder=6)
    ax.text(9.75, 1.2, 'Own data\n(Layer 2 CDO)', ha='left',
            fontsize=FS_SRC-4, color=GOLD, fontweight='bold')
    ax.text(9.4, 7.9, 'Combined source\n(inherited + own data)',
            ha='center', fontsize=FS_SRC-4, color=NAVY)

    bx2 = 12.0
    tc2, bc2 = mini_barrier(bx2)
    ax.text(bx2+0.35, 1.0, 'Layer 2\nAgents', ha='left', fontsize=FS_SRC-4, color=NAVY)

    for sc in [tc2, bc2]:
        ax.annotate('', xy=(bx2-.2, sc), xytext=(9.4, CY),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.4, alpha=0.45))
        ax.annotate('', xy=(bx2-.2, sc), xytext=(9.4, 1.2),
                    arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.2, alpha=0.45))

    arcs(bx2, tc2, bc2, 14.0, RED)

    # ── THREE OBSERVER SCREENS ────────────────────────────────────────────────
    # Each screen is at a different distance from Layer 2 agents.
    # Fringe spacing scales with distance: wider = further (Fraunhofer regime).
    # (sx, color, observer_label, regime_label, n_fringes, spacing)
    observer_screens = [
        (14.2, NAVY,  'Risk team',  'Fresnel',     9, 0.55),
        (17.0, GOLD,  'Board',      '',            7, 0.85),
        (19.8, RED,   'Regulator',  'Fraunhofer',  5, 1.25),
    ]

    for sx, col, obs_lbl, regime_lbl, n, sp in observer_screens:
        # Screen line
        ax.plot([sx, sx], [0.6, 8.8], color=col, lw=2.8, zorder=5)
        # Observer label above screen
        ax.text(sx, 9.0, obs_lbl, ha='center', va='bottom',
                fontsize=FS_ANNOT, color=col, fontweight='bold')
        # Regime label below screen
        if regime_lbl:
            ax.text(sx, 0.30, regime_lbl, ha='center', va='bottom',
                    fontsize=FS_ANNOT-2, color=col, style='italic')
        # Fringe dots on screen
        fringes(sx, col, n=n, spacing=sp)

    # Distance arrows from barrier to each screen
    arrow_y = 0.55
    for sx, col, _, _, _, _ in observer_screens:
        ax.annotate('', xy=(sx-0.05, arrow_y), xytext=(bx2+0.2, arrow_y),
                    arrowprops=dict(arrowstyle='<->', color=col, lw=1.0, alpha=0.55))

    # Annotation: same structure at every screen — placed between Board and Regulator
    ax.text(18.4, 7.2,
            'Same underlying pattern\nat every observation distance\n'
            '(wider fringe spacing = greater D)',
            ha='center', va='center', fontsize=FS_ANNOT-2, color=GRAY,
            style='italic',
            bbox=dict(boxstyle='round,pad=0.4', fc=WHITE, ec=GRAY, alpha=0.85))

    plt.tight_layout(rect=[0, 0.0, 1, 1])
    plt.savefig(f"{OUT}/fig10.png", dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(); print("fig10")


# ── FIG 11 ────────────────────────────────────────────────────────────────────
def fig11():
    """Compound failure rate (Finkel) as structural exposure G_N — all curves black."""
    # Color convention: RED = no governance (Finkel), used in Fig 12.
    # Here all curves are Finkel (no governance) at different g values —
    # differentiated by line style + marker only; g=20% heavier as it
    # is the reference case carried into Fig 12.
    BLK1 = "#111111"   # g=20% — heaviest, reference case
    BLK2 = "#333333"   # g=10%
    BLK3 = "#555555"   # g=5%
    BLK4 = "#888888"   # g=1%

    layers = np.arange(1, 9)
    configs = [
        (0.01, BLK4, '-.',  'o', 2.0, r'$g = 1\,\%$'),
        (0.05, BLK3, ':',   's', 2.0, r'$g = 5\,\%$'),
        (0.10, BLK2, '--',  '^', 2.0, r'$g = 10\,\%$'),
        (0.20, RED,  '-',   'D', 3.5, r'$g = 20\,\%$ (reference case — see Figure~12)'),
    ]

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)

    # MECE ideal: G_N = 0
    ax.axhline(0.0, color=NAVY, lw=2.0, ls='-', alpha=0.35, zorder=1)
    ax.text(1.1, 0.010, r'MECE ideal: $g = 0$ — zero structural exposure at every layer',
            ha='left', va='bottom', fontsize=FS_ANNOT-4, color=NAVY, fontweight='bold')

    for g, col, ls, mk, lw, lbl in configs:
        G = 1 - (1 - g) ** layers          # Finkel: G_N = 1 - (1-g)^N
        ax.plot(layers, G, marker=mk, ls=ls, color=col,
                lw=lw, ms=10, label=lbl, zorder=3)
        val = float(G[-1])
        ax.text(8.08, val, f'{val:.1%}',
                ha='left', va='center', fontsize=FS_ANNOT-4, color=col, fontweight='bold')

    ax.set_xlabel('Cascade layer $n$', fontsize=FS_AXIS, color=NAVY)
    ax.set_ylabel(r'Structural exposure $G_N$'
                  '\n(probability of structurally affected output at layer $N$)',
                  fontsize=FS_AXIS-2, color=NAVY)
    ax.set_title('Compound Failure Rate Across Cascade Layers\n'
                 r'(Finkel et al.\ upper bound: $f_n = 1$, $w_n = 1$, '
                 r'independent failure assumption)',
                 fontsize=FS_TITLE-1, color=NAVY, pad=10)
    ax.set_xlim(1, 9.8)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xticks(layers)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
    ax.tick_params(colors=NAVY, labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)

    ax.legend(fontsize=FS_LEG-2, framealpha=0.3, loc='upper left',
              title='Own-layer MECE gap $g$\n(constant at every layer)',
              title_fontsize=FS_ANNOT-4)

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig11.png", dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(); print("fig11")


def fig12():
    """Governance value: structural exposure G_N vs. Finkel upper bound."""
    import matplotlib.patches as mpatches

    layers = np.arange(1, 9)
    g = 0.20   # own-layer MECE gap, fixed at every layer

    # ── Compute G_n via recurrence G_1=g*f, G_n=f*(g + w*G_{n-1}*(1-g)) ─────
    # For all curves we set f=1 (no layer-level filtering), vary w → α = w*(1-g)
    # Ceiling: G_inf = f*g / (1 - alpha)  when f=1 → g / (1-alpha)
    def structural_exposure(alpha, g=0.20, f=1.0, n_layers=8):
        w = alpha / (1 - g)          # derive w from target alpha and g
        G = np.zeros(n_layers)
        G[0] = g * f                 # G_1
        for n in range(1, n_layers):
            G[n] = f * (g + w * G[n-1] * (1 - g))
        return G

    def finkel(g, n_layers=8):
        n = np.arange(1, n_layers + 1)
        return 1 - (1 - g) ** n

    G_finkel = finkel(g)

    # Color convention: RED = no governance (Finkel) — only red in this figure.
    # Governed curves: black/gray shades, varying line style + marker only.
    BLK1 = "#111111"   # strong governance   α=0.20
    BLK2 = "#444444"   # moderate governance α=0.50
    BLK3 = "#777777"   # weak governance     α=0.70

    # Governed curves: (alpha, color, linestyle, marker, label)
    governed = [
        (0.70, BLK3, '--', 's',
         r'$\alpha = 0.70$ — weak governance'
         '\n'
         r'($w=87.5\%$ inheritance, $f=100\%$ pass-through)'),
        (0.50, BLK2, '-.', '^',
         r'$\alpha = 0.50$ — moderate governance'
         '\n'
         r'($w=62.5\%$ inheritance, $f=100\%$ pass-through)'),
        (0.20, BLK1, ':',  'o',
         r'$\alpha = 0.20$ — strong governance'
         '\n'
         r'($w=25\%$ inheritance, $f=100\%$ pass-through)'),
    ]

    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)

    # ── Finkel curve (worst case, upper bound) — RED only ────────────────────
    ax.plot(layers, G_finkel, color=RED, lw=3.2, ls='-', marker='D', ms=10,
            label=r'No governance — Finkel et al.\ (upper bound, $\alpha = 0.80$)',
            zorder=5)
    ax.text(8.08, float(G_finkel[-1]),
            f'{float(G_finkel[-1]):.1%}',
            ha='left', va='center', fontsize=FS_ANNOT-4, color=RED, fontweight='bold')

    # ── Governed curves + ceiling lines + shading ─────────────────────────────
    for alpha, col, ls, mk, lbl in governed:
        G = structural_exposure(alpha, g=g)
        ceiling = g / (1 - alpha)

        # Shade between Finkel and this governed curve
        ax.fill_between(layers, G_finkel, G, alpha=0.07, color=col, zorder=1)

        # Governed G_n curve
        ax.plot(layers, G, color=col, lw=2.8, ls=ls, marker=mk, ms=10,
                label=lbl, zorder=4)

        # Finite ceiling dotted line
        ax.axhline(ceiling, color=col, lw=1.4, ls=':', alpha=0.65, zorder=2)
        ax.text(1.05, ceiling + 0.008,
                rf'$G_{{\infty}} = {ceiling:.3f}$',
                ha='left', va='bottom', fontsize=FS_ANNOT-5, color=col)

        # Endpoint annotation
        ax.text(8.08, float(G[-1]),
                f'{float(G[-1]):.1%}',
                ha='left', va='center', fontsize=FS_ANNOT-4, color=col, fontweight='bold')

    # ── MECE ideal reference ──────────────────────────────────────────────────
    ax.axhline(0.0, color=NAVY, lw=2.0, ls='-', alpha=0.30, zorder=1)
    ax.text(1.05, 0.005, r'MECE ideal: $G_N = 0$ (no structural exposure)',
            ha='left', va='bottom', fontsize=FS_ANNOT-5, color=NAVY, fontweight='bold')

    # ── Labels ────────────────────────────────────────────────────────────────
    ax.set_xlabel('Cascade layer $n$', fontsize=FS_AXIS, color=NAVY)
    ax.set_ylabel(r'Structural exposure $G_N$'
                  '\n(probability of structurally affected output at layer $N$)',
                  fontsize=FS_AXIS-3, color=NAVY)
    ax.set_title(
        r'Governance Value: Structural Exposure $G_N$ vs.\ Finkel Upper Bound'
        '\n'
        r'($g = 20\%$ own-layer MECE gap at every layer; shaded area = governance benefit)',
        fontsize=FS_TITLE-1, color=NAVY, pad=12)

    ax.set_xlim(1, 9.8)
    ax.set_ylim(-0.02, 1.05)
    ax.set_xticks(layers)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.tick_params(colors=NAVY, labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

    ax.legend(fontsize=FS_LEG-3, framealpha=0.35, loc='upper left',
              title=r'Transmission factor $\alpha = w \cdot f \cdot (1-g)$',
              title_fontsize=FS_ANNOT-4)

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig12.png", dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(); print("fig12")


def fig14():
    """
    Exponential convergence of Var(G_n) to the stationary variance sigma*^2.

    Demonstrates Bougerol (1993) Theorem 2.4: the distribution of G_n converges
    to the stationary distribution G* at exponential rate E[alpha^2] per layer.

    Left panel  — Var(G_n) vs n on a linear scale, converging to sigma*^2.
    Right panel — sigma*^2 - Var(G_n) on a LOG scale: straight lines prove
                  the convergence is exponential.  The slope of each line equals
                  log(E[alpha^2]), which differs by governance regime.

    This content is NOT in Figure 13 (which shows only the stationary distribution,
    not the speed of convergence to it).  Saves to fig14.png (Figure 14 in document).
    """
    beta_bar = 0.20
    var_beta = 0.0        # beta treated as deterministic — all variance from alpha
    CV_alpha = 0.30
    N        = 8
    layers   = np.arange(1, N + 1)

    configs = [
        (0.20, "#111111", "-",   r"Strong ($\bar{\alpha}=0.20$, $E[\alpha^2]=0.044$)"),
        (0.50, "#555555", "--",  r"Moderate ($\bar{\alpha}=0.50$, $E[\alpha^2]=0.273$)"),
        (0.70, "#999999", "-.",  r"Weak ($\bar{\alpha}=0.70$, $E[\alpha^2]=0.534$)"),
    ]

    fig, axes = plt.subplots(2, 1, figsize=(14, 16))
    fig.patch.set_facecolor(WHITE)

    for alpha_bar, col, ls, gov_label in configs:
        var_alpha = (CV_alpha * alpha_bar) ** 2
        E_alpha2  = var_alpha + alpha_bar ** 2
        E_beta2   = beta_bar ** 2           # = 0.04 (var_beta = 0)

        # Exact stationary moments
        mu_star  = beta_bar / (1.0 - alpha_bar)
        sigma2   = (var_alpha * mu_star**2 + var_beta) / (1.0 - E_alpha2)

        # Exact moment recursion: G_0 = 0
        m = np.zeros(N + 1)    # E[G_n]
        q = np.zeros(N + 1)    # E[G_n^2]
        for n in range(1, N + 1):
            m[n] = alpha_bar * m[n-1] + beta_bar
            # E[G_n^2] = E[α²]·E[G_{n-1}²] + 2·E[αβ]·E[G_{n-1}] + E[β²]
            # independence: E[αβ] = ᾱ·β̄
            q[n] = E_alpha2 * q[n-1] + 2.0 * alpha_bar * beta_bar * m[n-1] + E_beta2

        var_n = q[1:] - m[1:]**2    # Var(G_n) for n = 1..8

        # ── Upper panel: Var(G_n) / sigma*^2  →  1 ───────────────────────────
        ratio_n = var_n / sigma2          # normalised: converges to 1
        ax0 = axes[0]
        ax0.plot(layers, ratio_n * 100, color=col, lw=2.8, ls=ls, marker='o',
                 ms=10, zorder=4, label=gov_label)

        # ── Lower panel: remaining gap ratio (1 - ratio_n) on log scale ───────
        gap_ratio = 1.0 - ratio_n        # fraction of sigma*^2 still missing
        # Clip to 0.01% floor so strong-governance line stays visible
        gap_pct   = np.clip(gap_ratio * 100, 0.01, 100)
        ax1   = axes[1]
        slope_label = (gov_label + '\n'
                       + rf'rate $= E[\alpha^2] = {E_alpha2:.3f}$, '
                       + rf'$\log E[\alpha^2] = {np.log(E_alpha2):.2f}$')
        ax1.semilogy(layers, gap_pct, color=col, lw=2.8,
                     ls=ls, marker='o', ms=10, zorder=4, label=slope_label)

        # Annotate % gap remaining at layer 8 (only if meaningful)
        gap8 = float(gap_ratio[-1]) * 100
        if gap8 > 0.5:
            ax1.annotate(f'{gap8:.0f}% gap\nat layer 8',
                         xy=(8, gap8), xytext=(7.0, gap8 * (2.5 if gap8 < 50 else 0.45)),
                         fontsize=FS_ANNOT-7, color=col,
                         arrowprops=dict(arrowstyle='->', color=col, lw=1.0),
                         bbox=dict(boxstyle='round,pad=0.2', fc=WHITE, ec=col, alpha=0.8))
        elif gap8 <= 0.5:
            ax1.annotate(r'$<$0.1% gap at layer 8',
                         xy=(8, 0.012),
                         xytext=(5.0, 0.04),
                         fontsize=FS_ANNOT-7, color=col,
                         arrowprops=dict(arrowstyle='->', color=col, lw=1.0),
                         bbox=dict(boxstyle='round,pad=0.2', fc=WHITE, ec=col, alpha=0.8))

    # ── Upper panel formatting ────────────────────────────────────────────────
    ax0 = axes[0]
    ax0.axhline(100, color=NAVY, lw=1.5, ls='--', alpha=0.4, zorder=2)
    ax0.text(9.6, 100, r'$\sigma^{*2}$ (100%)', ha='left', va='center',
             fontsize=FS_ANNOT-7, color=NAVY)
    ax0.set_xlabel(r'Cascade layer $n$', fontsize=FS_AXIS, color=NAVY)
    ax0.set_ylabel(r'$\mathrm{Var}(G_n)\,/\,\sigma^{*2}$  [%]',
                   fontsize=FS_AXIS, color=NAVY)
    ax0.set_title(
        r'Normalised variance $\mathrm{Var}(G_n)/\sigma^{*2}$: '
        r'all regimes on the same scale' + '\n'
        r'(converges to 100%; exact moment recursion; $G_0=0$)',
        fontsize=FS_TITLE-2, color=NAVY, pad=10)
    ax0.set_xlim(0.8, 9.5)
    ax0.set_ylim(-2, 108)
    ax0.set_xticks(layers)
    ax0.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=100,
                                                                      decimals=0))
    ax0.tick_params(colors=NAVY, labelsize=FS_TICK)
    for sp in ax0.spines.values(): sp.set_color(NAVY)
    ax0.legend(fontsize=FS_LEG-5, framealpha=0.35, loc='upper left')
    ax0.grid(True, alpha=0.10, color=NAVY)

    # ── Lower panel formatting ────────────────────────────────────────────────
    ax1 = axes[1]
    ax1.axhline(100, color=NAVY, lw=1.0, ls='--', alpha=0.25, zorder=1)
    ax1.set_xlabel(r'Cascade layer $n$', fontsize=FS_AXIS, color=NAVY)
    ax1.set_ylabel(r'$1 - \mathrm{Var}(G_n)/\sigma^{*2}$  [%, log scale]',
                   fontsize=FS_AXIS, color=NAVY)
    ax1.set_title(
        r'Remaining gap ratio on log scale: straight lines $=$ exponential decay' + '\n'
        r'(Bougerol 1993, Thm 2.4; slope $= \log E[\alpha^2]$)',
        fontsize=FS_TITLE-2, color=NAVY, pad=10)
    ax1.set_xlim(0.8, 9.5)
    ax1.set_xticks(layers)
    ax1.set_ylim(0.005, 200)
    ax1.yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10,
                                                              subs=[1.0], numticks=8))
    ax1.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda y, _: f'{y:.0f}%' if y >= 1 else f'{y:.2f}%'))
    ax1.tick_params(colors=NAVY, labelsize=FS_TICK)
    for sp in ax1.spines.values(): sp.set_color(NAVY)
    ax1.legend(fontsize=FS_LEG-6, framealpha=0.35,
               loc='upper right', bbox_to_anchor=(1.0, 0.62))
    ax1.grid(True, alpha=0.10, color=NAVY, which='both')

    ax1.text(0.04, 0.05,
             'Steeper slope = faster convergence.\n'
             'All three lines are straight = exponential\n'
             'decay in every governance regime.\n'
             'Slope = log E[α²] (governance-dependent).',
             transform=ax1.transAxes, fontsize=FS_ANNOT-6, color=NAVY,
             va='bottom', ha='left',
             bbox=dict(boxstyle='round,pad=0.35', fc=WHITE, ec=NAVY, alpha=0.85))

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig14.png", dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close()
    print("fig14 (exponential convergence — Bougerol Thm 2.4)")


def fig13():
    """
    Stationary distribution of G* as a probability density (PDF).

    Uses the Brandt (1986) exact second-moment analysis:
        mu*    = beta_bar / (1 - alpha_bar)
        sigma2 = [Var(alpha) * mu*^2 + Var(beta)] / (1 - E[alpha^2])

    The stationary distribution is approximated by Beta(a, b) fitted to
    (mu*, sigma2).  Three governance regimes are shown as PDFs so the
    reader sees WHERE risk mass is concentrated, not a cumulative curve.
    A narrow peak near 0 = risk well contained; a broad spread toward 1
    = risk mass approaching the Finkel limit (certain structural failure).
    """
    from scipy.stats import beta as beta_dist

    # ── Fixed structural parameters ───────────────────────────────────────────
    beta_bar = 0.20
    var_beta = 0.0
    CV_alpha = 0.30

    configs = [
        (0.20, "#111111", "-",   r"Strong governance ($\bar{\alpha}=0.20$)"),
        (0.50, "#555555", "--",  r"Moderate governance ($\bar{\alpha}=0.50$)"),
        (0.70, "#999999", "-.",  r"Weak governance ($\bar{\alpha}=0.70$)"),
    ]

    x = np.linspace(0.001, 0.999, 3000)

    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)

    for alpha_bar, col, ls, gov_label in configs:
        var_alpha = (CV_alpha * alpha_bar) ** 2
        E_alpha2  = var_alpha + alpha_bar ** 2
        mu_star   = beta_bar / (1.0 - alpha_bar)
        sigma2    = (var_alpha * mu_star**2 + var_beta) / (1.0 - E_alpha2)

        k = mu_star * (1.0 - mu_star) / sigma2 - 1.0
        a = mu_star * k
        b = (1.0 - mu_star) * k

        pdf = beta_dist.pdf(x, a, b)

        # Mode of the Beta(a,b) distribution (only defined when a,b > 1)
        if a > 1 and b > 1:
            mode = (a - 1.0) / (a + b - 2.0)
        else:
            mode = None

        lbl = (f"{gov_label}\n"
               r"$\mu^*=" + f"{mu_star:.2f}"
               r",\ \sigma^{*2}=" + f"{sigma2:.4f}"
               r",\ \mathbb{{E}}[\alpha^2]=" + f"{E_alpha2:.3f}" + r"$")

        lw = 3.0 if col == "#111111" else 2.2
        ax.plot(x, pdf, color=col, lw=lw, ls=ls, zorder=4, label=lbl)

        # Mark the mode with a vertical tick
        if mode is not None:
            peak_pdf = beta_dist.pdf(mode, a, b)
            ax.plot([mode, mode], [0, peak_pdf], color=col, lw=1.0,
                    ls=':', alpha=0.55, zorder=3)

    # ── Labels and axes (set before arrow so ylim is known) ──────────────────
    ax.set_xlabel(r'Stationary structural exposure $G^*$', fontsize=FS_AXIS, color=NAVY)
    ax.set_ylabel(r'Probability density', fontsize=FS_AXIS, color=NAVY)
    ax.set_title(
        r'Where Does Risk Mass Concentrate? Stationary Distribution of $G^*$ by Governance Regime' + '\n'
        r'Exact moments (Brandt 1986); Beta$(a,b)$ approximation; '
        r'$\bar{\beta}=0.20$, $\mathrm{CV}_\alpha=30\%$',
        fontsize=FS_TITLE-2, color=NAVY, pad=12)

    ax.set_xlim(-0.01, 1.10)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.tick_params(colors=NAVY, labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    ax.grid(True, alpha=0.12, color=NAVY)

    # ── Finkel limit: Dirac delta at G* = 1 ──────────────────────────────────
    # As alpha_bar → 1, the Beta(a,b) distribution collapses to δ(G* − 1).
    # Shown as an impulse arrow (standard convention for Dirac delta).
    # Use the strong-governance peak height as reference for arrow scaling.
    from scipy.stats import beta as _bd
    _ab = 0.20; _va = (CV_alpha*_ab)**2; _ea2 = _va+_ab**2
    _mu = beta_bar/(1-_ab); _s2 = (_va*_mu**2+var_beta)/(1-_ea2)
    _k = _mu*(1-_mu)/_s2 - 1; _a = _mu*_k; _b = (1-_mu)*_k
    peak_ref = _bd.pdf((_a-1)/(_a+_b-2), _a, _b)  # mode of strong-gov dist
    arrow_h = peak_ref * 0.80

    ax.annotate('', xy=(1.0, arrow_h), xytext=(1.0, 0.0),
                arrowprops=dict(arrowstyle='->', color=RED, lw=3.0,
                                mutation_scale=18), zorder=6)
    ax.text(0.978, arrow_h * 0.48,
            r'$\delta(G^*\!-\!1)$' + '\nFinkel limit\n' + r'($\bar{\alpha}\!\to\!1$)',
            fontsize=FS_ANNOT-6, color=RED, ha='right', va='center', zorder=7,
            bbox=dict(boxstyle='round,pad=0.25', fc=WHITE, ec=RED, alpha=0.88))
    ax.plot([], [], color=RED, lw=2.5,
            label=r'Finkel limit: $\bar{\alpha}\!\to\!1\ \Rightarrow\ \delta(G^*\!-\!1)$')

    # ── Risk-readable annotation ──────────────────────────────────────────────
    ax.text(0.03, 0.97,
            'Narrow peak near 0%:\nrisk mass well contained.\n\n'
            'Broad spread toward 100%:\nrisk mass approaching\nthe Finkel limit.',
            transform=ax.transAxes, fontsize=FS_ANNOT-5, color=NAVY,
            va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.4', fc=WHITE, ec=NAVY, alpha=0.85))

    ax.legend(fontsize=FS_LEG-4, framealpha=0.40, loc='upper right',
              title=r'Governance regime (transmission factor $\bar{\alpha}$)',
              title_fontsize=FS_ANNOT-5)

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig13.png", dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(); print("fig13 (Beta PDF — risk mass concentration + Finkel delta)")


def fig15():
    """
    Tail exceedance probability P(G* > tau) = 1 - I_tau(a,b)
    for the three governance regimes.

    Companion to Figure 13 (CDF): Figure 13 shows where the cascade
    tends to; Figure 15 shows the probability of exceeding any given
    risk threshold.  Uses identical parameter choices to Figure 13.
    """
    from scipy.stats import beta as beta_dist

    # ── Fixed structural parameters (identical to Figure 13) ─────────────────
    beta_bar = 0.20
    var_beta = 0.0
    CV_alpha = 0.30

    configs = [
        (0.20, "#111111", "-",   r"Strong governance ($\bar{\alpha}=0.20$)"),
        (0.50, "#555555", "--",  r"Moderate governance ($\bar{\alpha}=0.50$)"),
        (0.70, "#999999", "-.",  r"Weak governance ($\bar{\alpha}=0.70$)"),
    ]

    tau = np.linspace(0.001, 0.999, 3000)

    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)

    for alpha_bar, col, ls, gov_label in configs:
        var_alpha = (CV_alpha * alpha_bar) ** 2
        E_alpha2  = var_alpha + alpha_bar ** 2
        mu_star   = beta_bar / (1.0 - alpha_bar)
        sigma2    = (var_alpha * mu_star**2 + var_beta) / (1.0 - E_alpha2)

        k = mu_star * (1.0 - mu_star) / sigma2 - 1.0
        a = mu_star * k
        b = (1.0 - mu_star) * k

        exceedance = 1.0 - beta_dist.cdf(tau, a, b)

        lw = 3.0 if col == "#111111" else 2.2
        ax.plot(tau, exceedance, color=col, lw=lw, ls=ls, zorder=4, label=gov_label)

        # Annotate at tau = 0.80 where spread is informative
        p_80 = 1.0 - beta_dist.cdf(0.80, a, b)
        if p_80 > 1e-4:   # only label if visible
            ax.plot(0.80, p_80, 'o', color=col, ms=9, zorder=6)
            lbl_str = f'{100*p_80:.2f}%' if p_80 < 0.01 else f'{100*p_80:.1f}%'
            ax.text(0.81, p_80, lbl_str,
                    ha='left', va='center',
                    fontsize=FS_ANNOT-5, color=col, fontweight='bold')

    # ── Finkel limit ──────────────────────────────────────────────────────────
    ax.axvline(1.0, color=RED, lw=2.5, ls='--', zorder=5,
               label=r'Finkel limit: $G^*=1$ (certain structural failure)')

    # ── Vertical reference lines at key thresholds ───────────────────────────
    for tau_ref, lbl in [(0.5, '50%'), (0.7, '70%'), (0.8, '80%'), (0.9, '90%')]:
        ax.axvline(tau_ref, color=NAVY, lw=0.8, ls=':', alpha=0.25)
        ax.text(tau_ref + 0.005, 1.00, lbl,
                ha='left', va='top',
                fontsize=FS_ANNOT-8, color=NAVY, alpha=0.55)

    # ── Labels ────────────────────────────────────────────────────────────────
    ax.set_xlabel(r'Structural exposure threshold $\tau$',
                  fontsize=FS_AXIS, color=NAVY)
    ax.set_ylabel(r'Exceedance probability $P(G^* > \tau) = 1 - I_\tau(a,b)$',
                  fontsize=FS_AXIS, color=NAVY)
    ax.set_title(
        r'Tail Risk of Stationary Structural Exposure by Governance Regime' + '\n'
        r'Exact moments (Brandt 1986); Beta$(a,b)$ approximation; '
        r'$\bar{\beta}=0.20$, $\mathrm{CV}_\alpha=30\%$',
        fontsize=FS_TITLE-2, color=NAVY, pad=12)

    ax.set_xlim(-0.01, 1.06)
    ax.set_ylim(-0.02, 1.04)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.tick_params(colors=NAVY, labelsize=FS_TICK)
    for sp in ax.spines.values(): sp.set_color(NAVY)
    ax.grid(True, alpha=0.12, color=NAVY)

    ax.legend(fontsize=FS_LEG-4, framealpha=0.40, loc='upper right',
              title=r'Governance regime (transmission factor $\bar{\alpha}$)',
              title_fontsize=FS_ANNOT-5)

    # ── Governance callout annotation ─────────────────────────────────────────
    ax.annotate(
        u'Same α̅ ∈ (0,1) condition;\n'
        'order-of-magnitude difference\nin tail risk at every threshold.',
        xy=(0.75, 0.06), xytext=(0.50, 0.30),
        fontsize=FS_ANNOT-5, color=NAVY,
        arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.2),
        bbox=dict(boxstyle='round,pad=0.35', fc=WHITE, ec=NAVY, alpha=0.85))

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig14.png", dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(); print("fig14 (tail exceedance)")


fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7(); fig8(); fig9()
fig10(); fig11(); fig12(); fig13(); fig14()  # fig15 removed (tail exceedance replaced by Bougerol fig14)
print("ALL DONE")
