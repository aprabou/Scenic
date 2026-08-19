"""Integration tests for signal↔maneuver linking via inline OpenDRIVE fixtures."""

from pathlib import Path

from scenic.domains.driving.roads import ManeuverType, Network

# Minimal maps exercised below (same geometries as the local demo/signals maps).
MAP_VALIDITY_LANES = """<?xml version="1.0" encoding="UTF-8"?>
<OpenDRIVE>
  <header revMajor="1" revMinor="6" name="signal_validity_lanes" version="1.0"/>
  <road name="West Approach" length="20.0" id="1" junction="-1" rule="RHT">
    <link><successor elementType="junction" elementId="100"/></link>
    <planView>
      <geometry s="0" x="0.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><successor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="East Exit" length="20.0" id="2" junction="-1" rule="RHT">
    <link><predecessor elementType="junction" elementId="100"/></link>
    <planView>
      <geometry s="0" x="32.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><predecessor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="Straight Connector" length="12.0" id="10" junction="100" rule="RHT">
    <link>
      <predecessor elementType="road" elementId="1" contactPoint="end"/>
      <successor elementType="road" elementId="2" contactPoint="start"/>
    </link>
    <planView>
      <geometry s="0" x="20.0" y="0.0" hdg="0.0" length="12.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><predecessor id="-2"/><successor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
    <signals>
      <signal s="1.0" t="-1.75" id="101" name="light_lane_m1" dynamic="yes"
              orientation="+" zOffset="5" type="1000001" country="OpenDRIVE"
              subtype="-1" value="-1">
        <validity fromLane="-1" toLane="-1"/>
      </signal>
      <signal s="1.0" t="-5.25" id="102" name="light_lane_m2" dynamic="yes"
              orientation="+" zOffset="5" type="1000001" country="OpenDRIVE"
              subtype="-1" value="-1">
        <validity fromLane="-2" toLane="-2"/>
      </signal>
    </signals>
  </road>
  <junction name="StraightSignalized" id="100">
    <connection id="0" incomingRoad="1" connectingRoad="10" contactPoint="start">
      <laneLink from="-1" to="-1"/>
      <laneLink from="-2" to="-2"/>
    </connection>
  </junction>
</OpenDRIVE>
"""

MAP_APPROACH_SIGNAL = """<?xml version="1.0" encoding="UTF-8"?>
<OpenDRIVE>
  <header revMajor="1" revMinor="6" name="signal_on_approach" version="1.0"/>
  <road name="West Approach" length="20.0" id="1" junction="-1" rule="RHT">
    <link><successor elementType="junction" elementId="100"/></link>
    <planView>
      <geometry s="0" x="0.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><successor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
    <signals>
      <signal s="18.0" t="-3.5" id="201" name="approach_light" dynamic="yes"
              orientation="+" zOffset="5" type="1000001" country="OpenDRIVE"
              subtype="-1" value="-1"/>
    </signals>
  </road>
  <road name="East Exit" length="20.0" id="2" junction="-1" rule="RHT">
    <link><predecessor elementType="junction" elementId="100"/></link>
    <planView>
      <geometry s="0" x="32.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><predecessor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="Straight Connector" length="12.0" id="10" junction="100" rule="RHT">
    <link>
      <predecessor elementType="road" elementId="1" contactPoint="end"/>
      <successor elementType="road" elementId="2" contactPoint="start"/>
    </link>
    <planView>
      <geometry s="0" x="20.0" y="0.0" hdg="0.0" length="12.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><predecessor id="-2"/><successor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <junction name="ApproachSignalized" id="100">
    <connection id="0" incomingRoad="1" connectingRoad="10" contactPoint="start">
      <laneLink from="-1" to="-1"/>
      <laneLink from="-2" to="-2"/>
    </connection>
  </junction>
</OpenDRIVE>
"""

# Town01-style: dummy validity 0-0, pole next to the junction, orientation
# names the other travel direction (CARLA lamp facing, not lane validity).
MAP_CARLA_DUMMY_VALIDITY = MAP_APPROACH_SIGNAL.replace(
    'orientation="+" zOffset="5" type="1000001" country="OpenDRIVE"\n'
    '              subtype="-1" value="-1"/>',
    'orientation="-" zOffset="5" type="1000001" country="OpenDRIVE"\n'
    '              subtype="-1" value="-1">\n'
    '        <validity fromLane="0" toLane="0"/>\n'
    "      </signal>",
)

MAP_T_JUNCTION = """<?xml version="1.0" encoding="UTF-8"?>
<OpenDRIVE>
  <header revMajor="1" revMinor="6" name="t_junction_turn_signals" version="1.0"/>
  <road name="West Approach" length="20.0" id="1" junction="-1" rule="RHT">
    <link><successor elementType="junction" elementId="200"/></link>
    <planView>
      <geometry s="0" x="0.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="East Exit" length="20.0" id="2" junction="-1" rule="RHT">
    <link><predecessor elementType="junction" elementId="200"/></link>
    <planView>
      <geometry s="0" x="32.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="South Exit" length="20.0" id="3" junction="-1" rule="RHT">
    <link><predecessor elementType="junction" elementId="200"/></link>
    <planView>
      <geometry s="0" x="26.0" y="-6.0" hdg="-1.5707963267948966" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="Straight Connector" length="12.0" id="10" junction="200" rule="RHT">
    <link>
      <predecessor elementType="road" elementId="1" contactPoint="end"/>
      <successor elementType="road" elementId="2" contactPoint="start"/>
    </link>
    <planView>
      <geometry s="0" x="20.0" y="0.0" hdg="0.0" length="12.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
    <signals>
      <signal s="1.0" t="-1.75" id="301" name="straight_light" dynamic="yes"
              orientation="+" zOffset="5" type="1000001" country="OpenDRIVE"
              subtype="-1" value="-1">
        <validity fromLane="-1" toLane="-1"/>
      </signal>
    </signals>
  </road>
  <road name="Right Turn Connector" length="12.0" id="11" junction="200" rule="RHT">
    <link>
      <predecessor elementType="road" elementId="1" contactPoint="end"/>
      <successor elementType="road" elementId="3" contactPoint="start"/>
    </link>
    <planView>
      <geometry s="0" x="20.0" y="0" hdg="0.0" length="6.0"><line/></geometry>
      <geometry s="6.0" x="26.0" y="0" hdg="-1.5707963267948966" length="6.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
    <signals>
      <signal s="1.0" t="-1.75" id="302" name="right_turn_arrow" dynamic="yes"
              orientation="+" zOffset="5" type="1000001" country="OpenDRIVE"
              subtype="-1" value="-1">
        <validity fromLane="-1" toLane="-1"/>
      </signal>
    </signals>
  </road>
  <junction name="TJunctionSignals" id="200">
    <connection id="0" incomingRoad="1" connectingRoad="10" contactPoint="start">
      <laneLink from="-1" to="-1"/>
    </connection>
    <connection id="1" incomingRoad="1" connectingRoad="11" contactPoint="start">
      <laneLink from="-1" to="-1"/>
    </connection>
  </junction>
</OpenDRIVE>
"""

MAP_UNSIGNALIZED = """<?xml version="1.0" encoding="UTF-8"?>
<OpenDRIVE>
  <header revMajor="1" revMinor="6" name="unsignalized_straight" version="1.0"/>
  <road name="West Approach" length="20.0" id="1" junction="-1" rule="RHT">
    <link><successor elementType="junction" elementId="100"/></link>
    <planView>
      <geometry s="0" x="0.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><successor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="East Exit" length="20.0" id="2" junction="-1" rule="RHT">
    <link><predecessor elementType="junction" elementId="100"/></link>
    <planView>
      <geometry s="0" x="32.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><predecessor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <road name="Straight Connector" length="12.0" id="10" junction="100" rule="RHT">
    <link>
      <predecessor elementType="road" elementId="1" contactPoint="end"/>
      <successor elementType="road" elementId="2" contactPoint="start"/>
    </link>
    <planView>
      <geometry s="0" x="20.0" y="0.0" hdg="0.0" length="12.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <link><predecessor id="-1"/><successor id="-1"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
          <lane id="-2" type="driving" level="false">
            <link><predecessor id="-2"/><successor id="-2"/></link>
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
      </laneSection>
    </lanes>
  </road>
  <junction name="Unsignalized" id="100">
    <connection id="0" incomingRoad="1" connectingRoad="10" contactPoint="start">
      <laneLink from="-1" to="-1"/>
      <laneLink from="-2" to="-2"/>
    </connection>
  </junction>
</OpenDRIVE>
"""


def load_network(tmp_path: Path, xml: str) -> Network:
    path = tmp_path / "map.xodr"
    path.write_text(xml)
    return Network.fromFile(path, useCache=False)


def open_drive_id(lane) -> int:
    ids = {sec.openDriveID for sec in lane.sections}
    assert len(ids) == 1, lane
    return next(iter(ids))


def all_maneuvers(network: Network):
    return [m for inter in network.intersections for m in inter.maneuvers]


def assert_bidirectional(maneuver):
    assert maneuver.signal is not None
    assert maneuver in maneuver.signal.controlledManeuvers
    for other in maneuver.signal.controlledManeuvers:
        assert other.signal is maneuver.signal


def test_validity_lanes_per_lane_signals(tmp_path):
    network = load_network(tmp_path, MAP_VALIDITY_LANES)
    mans = all_maneuvers(network)
    assert len(mans) == 2

    by_start = {open_drive_id(m.startLane): m for m in mans}
    assert set(by_start) == {-1, -2}

    man_inner, man_outer = by_start[-1], by_start[-2]
    assert man_inner.type is ManeuverType.STRAIGHT
    assert man_outer.type is ManeuverType.STRAIGHT
    assert man_inner.signal.openDriveID == "101"
    assert man_outer.signal.openDriveID == "102"
    assert man_inner.signal is not man_outer.signal
    assert man_inner.signal.isTrafficLight
    assert_bidirectional(man_inner)
    assert_bidirectional(man_outer)
    assert man_inner.signal.controlledManeuvers == (man_inner,)
    assert man_outer.signal.controlledManeuvers == (man_outer,)


def test_approach_signal_shared_by_both_lanes(tmp_path):
    network = load_network(tmp_path, MAP_APPROACH_SIGNAL)
    mans = all_maneuvers(network)
    assert len(mans) == 2
    assert mans[0].signal is mans[1].signal
    assert mans[0].signal.openDriveID == "201"
    for man in mans:
        assert_bidirectional(man)
    assert set(mans[0].signal.controlledManeuvers) == set(mans)


def test_t_junction_distinct_signals_per_maneuver(tmp_path):
    network = load_network(tmp_path, MAP_T_JUNCTION)
    mans = all_maneuvers(network)
    assert len(mans) == 2

    by_type = {m.type: m for m in mans}
    assert set(by_type) == {ManeuverType.STRAIGHT, ManeuverType.RIGHT_TURN}
    assert (
        by_type[ManeuverType.STRAIGHT].startLane
        is by_type[ManeuverType.RIGHT_TURN].startLane
    )

    straight, right = by_type[ManeuverType.STRAIGHT], by_type[ManeuverType.RIGHT_TURN]
    assert straight.signal.openDriveID == "301"
    assert right.signal.openDriveID == "302"
    assert straight.signal is not right.signal
    assert_bidirectional(straight)
    assert_bidirectional(right)


def test_unsignalized_maneuvers_have_no_signal(tmp_path):
    network = load_network(tmp_path, MAP_UNSIGNALIZED)
    mans = all_maneuvers(network)
    assert len(mans) == 2
    assert all(m.signal is None for m in mans)
    for road in list(network.roads) + list(network.connectingRoads):
        for sig in road.signals:
            assert sig.controlledManeuvers == ()


def test_intersection_backrefs_consistent(tmp_path):
    for xml in (
        MAP_VALIDITY_LANES,
        MAP_APPROACH_SIGNAL,
        MAP_T_JUNCTION,
        MAP_UNSIGNALIZED,
    ):
        network = load_network(tmp_path, xml)
        for inter in network.intersections:
            for man in inter.maneuvers:
                assert man.intersection is inter
                if man.signal is not None:
                    assert_bidirectional(man)
                    assert man.signal.isTrafficLight


# ---------------------------------------------------------------------------
# Legacy OpenDRIVE type codes (CARLA: 1000001 / 206 / 205) and 1.8+ priorities
# ---------------------------------------------------------------------------

DEMO_SIGNALS = (
    Path(__file__).resolve().parents[3] / "assets" / "maps" / "demo" / "signals"
)


def test_legacy_stop_and_yield_type_codes():
    """CARLA maps use country=OpenDRIVE type 206 (stop) and 205 (yield)."""
    network = Network.fromFile(DEMO_SIGNALS / "06_legacy_stop_yield.xodr", useCache=False)
    by_start = {open_drive_id(m.startLane): m for m in all_maneuvers(network)}
    assert set(by_start) == {-1, -2}

    stop_man, yield_man = by_start[-1], by_start[-2]
    assert stop_man.signal.openDriveID == "601"
    assert yield_man.signal.openDriveID == "602"

    assert stop_man.signal.priorities == ()
    assert yield_man.signal.priorities == ()
    assert stop_man.signal.type == "206"
    assert yield_man.signal.type == "205"

    assert stop_man.signal.isStop
    assert not stop_man.signal.isYield
    assert not stop_man.signal.isTrafficLight

    assert yield_man.signal.isYield
    assert not yield_man.signal.isStop
    assert not yield_man.signal.isTrafficLight

    assert_bidirectional(stop_man)
    assert_bidirectional(yield_man)


def test_priority_semantics_without_legacy_types():
    """``<priority>`` classifies signals even when country type is uninformative."""
    from scenic.domains.driving.roads import SignalPriorityType

    network = Network.fromFile(
        DEMO_SIGNALS / "07_priority_semantics.xodr", useCache=False
    )
    by_start = {open_drive_id(m.startLane): m for m in all_maneuvers(network)}
    assert set(by_start) == {-1, -2, -3}

    stop_man, yield_man, light_man = by_start[-1], by_start[-2], by_start[-3]
    assert stop_man.signal.type == "-1"
    assert yield_man.signal.type == "-1"
    assert light_man.signal.type == "-1"

    assert stop_man.signal.isStop
    assert not stop_man.signal.isTrafficLight
    assert stop_man.signal.priorities == (SignalPriorityType.STOP,)

    assert yield_man.signal.isYield
    assert not yield_man.signal.isStop
    assert yield_man.signal.priorities == (SignalPriorityType.YIELD,)

    assert light_man.signal.isTrafficLight
    assert light_man.signal.isStopLine
    assert not light_man.signal.isStop
    assert light_man.signal.priorities == (
        SignalPriorityType.TRAFFIC_LIGHT,
        SignalPriorityType.STOP_LINE,
    )

    for man in (stop_man, yield_man, light_man):
        assert_bidirectional(man)


def test_updated_traffic_light_demo_maps_have_priorities():
    """Regenerated TL demos keep type 1000001 and add ``<priority type="trafficLight"/>``."""
    from scenic.domains.driving.roads import SignalPriorityType

    for name in (
        "01_signal_validity_lanes.xodr",
        "02_signal_on_approach.xodr",
        "03_t_junction_turn_signals.xodr",
        "05_four_way_protected_left.xodr",
    ):
        network = Network.fromFile(DEMO_SIGNALS / name, useCache=False)
        signals = [
            sig
            for road in list(network.roads) + list(network.connectingRoads)
            for sig in road.signals
        ]
        assert signals, name
        for sig in signals:
            assert sig.type == "1000001", (name, sig.openDriveID)
            assert SignalPriorityType.TRAFFIC_LIGHT in sig.priorities, (
                name,
                sig.openDriveID,
            )
            assert sig.isTrafficLight
            assert not sig.isStop
            assert not sig.isYield


def test_legacy_traffic_light_fixture_still_works(tmp_path):
    """Inline fixtures without ``<semantics>`` still detect type 1000001 lights."""
    network = load_network(tmp_path, MAP_VALIDITY_LANES)
    for man in all_maneuvers(network):
        assert man.signal.priorities == ()
        assert man.signal.isTrafficLight
        assert man.signal.subtype == "-1"


def test_priority_type_disagreement_warns_and_prefers_priorities(tmp_path):
    """Legacy type and ``<priority>`` disagree → warn; priorities win."""
    import warnings

    from scenic.domains.driving.roads import SignalPriorityType
    from scenic.formats.opendrive.xodr_parser import OpenDriveWarning

    # Same geometry as MAP_VALIDITY_LANES but type 206 (stop) with trafficLight priority.
    xml = MAP_VALIDITY_LANES.replace(
        'type="1000001" country="OpenDRIVE"\n              subtype="-1" value="-1">\n'
        '        <validity fromLane="-1" toLane="-1"/>\n'
        "      </signal>",
        'type="206" country="OpenDRIVE"\n              subtype="-1" value="-1">\n'
        "        <semantics>\n"
        '          <priority type="trafficLight"/>\n'
        "        </semantics>\n"
        '        <validity fromLane="-1" toLane="-1"/>\n'
        "      </signal>",
        1,  # only the first signal (id 101)
    )
    # Second signal unchanged (still legacy 1000001, no semantics).

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", OpenDriveWarning)
        network = load_network(tmp_path, xml)

    disagreement = [
        w
        for w in caught
        if issubclass(w.category, OpenDriveWarning)
        and "using priorities for classification" in str(w.message)
        and 'type "206"' in str(w.message)
    ]
    assert len(disagreement) == 1, [str(w.message) for w in caught]

    by_start = {open_drive_id(m.startLane): m for m in all_maneuvers(network)}
    # Lane -1: priorities win → traffic light, not stop
    assert by_start[-1].signal.isTrafficLight
    assert not by_start[-1].signal.isStop
    assert SignalPriorityType.TRAFFIC_LIGHT in by_start[-1].signal.priorities
    # Lane -2: unchanged legacy light
    assert by_start[-2].signal.isTrafficLight
    assert by_start[-2].signal.priorities == ()


# Placement / <reference> / deprecated <positionRoad> (stop-line derivation).
# One road, two travel directions, three signals:
#   1 — 1.8+ light that <reference>s a stop line
#   2 — the stop line
#   3 — pre-1.8 logical-s signal with <positionRoad> pole offset
MAP_SIGNAL_PLACEMENT = """<?xml version="1.0" encoding="UTF-8"?>
<OpenDRIVE>
  <header revMajor="1" revMinor="8" name="signal_placement" version="1.0"/>
  <road name="TwoWay" length="20.0" id="1" junction="-1" rule="RHT">
    <planView>
      <geometry s="0" x="0.0" y="0.0" hdg="0.0" length="20.0"><line/></geometry>
    </planView>
    <lanes>
      <laneOffset s="0" a="0" b="0" c="0" d="0"/>
      <laneSection s="0">
        <center><lane id="0" type="none" level="false"/></center>
        <right>
          <lane id="-1" type="driving" level="false">
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </right>
        <left>
          <lane id="1" type="driving" level="false">
            <width sOffset="0" a="3.5" b="0" c="0" d="0"/>
          </lane>
        </left>
      </laneSection>
    </lanes>
    <signals>
      <signal s="2.0" t="-4.0" id="1" name="light" dynamic="yes"
              orientation="+" zOffset="5" type="1000001" country="OpenDRIVE"
              subtype="-1" value="-1">
        <validity fromLane="-1" toLane="-1"/>
        <reference elementId="2" elementType="signal" type="stopline"/>
      </signal>
      <signal s="18.0" t="0.0" id="2" name="stop_line" dynamic="no"
              orientation="none" zOffset="0" type="-1" country="OpenDRIVE"
              subtype="-1" value="-1">
        <semantics><priority type="stopLine"/></semantics>
      </signal>
      <signal s="10.0" t="-1.75" id="3" name="legacy_logical" dynamic="no"
              orientation="-" zOffset="2" type="206" country="OpenDRIVE"
              subtype="-1" value="-1">
        <positionRoad roadId="1" s="12.0" t="-4.0" zOffset="2" hOffset="0"/>
      </signal>
    </signals>
  </road>
</OpenDRIVE>
"""


def _signals_by_id(network):
    return {sig.openDriveID: sig for road in network.roads for sig in road.signals}


def test_validity_lanes_expose_placement_and_affects(tmp_path):
    """Existing per-lane lights keep s/t/validity; affects() follows validity."""
    network = load_network(tmp_path, MAP_VALIDITY_LANES)
    by_start = {open_drive_id(m.startLane): m for m in all_maneuvers(network)}
    for lid, man in by_start.items():
        sig = man.signal
        assert sig.s == 1.0
        assert sig.t is not None
        assert sig.orientation == "+"
        assert sig.validity is not None
        lo, hi = sig.validity
        assert lo <= lid <= hi
        assert sig.affects(man.startLane)
        assert not sig.sIsLogical
        assert sig.references == ()
        for other_lid, other in by_start.items():
            if other_lid != lid and not (lo <= other_lid <= hi):
                assert not sig.affects(other.startLane)


def test_signal_reference_and_logical_s_parsed(tmp_path):
    """<reference> and deprecated <positionRoad> survive conversion."""
    from scenic.domains.driving.roads import SignalLink

    network = load_network(tmp_path, MAP_SIGNAL_PLACEMENT)
    by_id = _signals_by_id(network)

    light = by_id["1"]
    assert light.s == 2.0
    assert light.t == -4.0
    assert light.orientation == "+"
    assert light.validity == (-1, -1)
    assert not light.sIsLogical
    assert light.references == (
        SignalLink(elementId="2", elementType="signal", type="stopline"),
    )
    assert light.stoppingS == 18.0  # referenced stop line, not the pole

    line = by_id["2"]
    assert line.s == 18.0
    assert line.isStopLine
    assert line.orientation == "none"
    assert line.references == ()
    assert line.stoppingS == 18.0

    legacy = by_id["3"]
    assert legacy.s == 10.0
    assert legacy.sIsLogical
    assert legacy.orientation == "-"
    assert legacy.isStop
    assert legacy.stoppingS == 10.0  # logical @s, not <positionRoad>


def test_affects_uses_validity_then_orientation(tmp_path):
    """orientation=none spans both directions; +/- and validity restrict."""
    network = load_network(tmp_path, MAP_SIGNAL_PLACEMENT)
    by_id = _signals_by_id(network)
    forward = next(lane for lane in network.roads[0].lanes if open_drive_id(lane) == -1)
    backward = next(lane for lane in network.roads[0].lanes if open_drive_id(lane) == 1)

    light = by_id["1"]
    assert light.affects(forward)
    assert not light.affects(backward)

    line = by_id["2"]
    assert line.affects(forward)
    assert line.affects(backward)

    legacy = by_id["3"]
    assert not legacy.affects(forward)
    assert legacy.affects(backward)


def test_carla_style_light_stops_at_junction_contact(tmp_path):
    """Pole-only approach light: halt at the junction, not at the pole ``s``."""
    network = load_network(tmp_path, MAP_APPROACH_SIGNAL)
    light = _signals_by_id(network)["201"]
    assert light.s == 18.0
    assert light.isTrafficLight
    assert light.references == ()
    assert not light.sIsLogical
    assert light.stoppingS == 20.0


def test_connector_light_has_no_invented_stopping_s(tmp_path):
    """Lights on a connecting road have no junction-contact fallback."""
    network = load_network(tmp_path, MAP_VALIDITY_LANES)
    for man in all_maneuvers(network):
        assert man.signal.s == 1.0
        assert man.signal.stoppingS is None
        assert man.signal.stoppingPointOn(man.startLane) is None


def _xy(pt, x, y, tol=0.05):
    assert pt is not None
    assert abs(pt.x - x) < tol, (pt.x, x)
    assert abs(pt.y - y) < tol, (pt.y, y)


def test_stopping_point_on_uses_station_not_pole(tmp_path):
    """Same stoppingS, both directions: different lane points, not the pole t."""
    network = load_network(tmp_path, MAP_SIGNAL_PLACEMENT)
    by_id = _signals_by_id(network)
    road = network.roads[0]
    forward = next(lane for lane in road.lanes if open_drive_id(lane) == -1)
    backward = next(lane for lane in road.lanes if open_drive_id(lane) == 1)

    light = by_id["1"]
    _xy(light.position, 2.0, -4.0)
    _xy(light.stoppingPointOn(forward), 18.0, -1.75)
    assert light.stoppingPointOn(backward) is None

    line = by_id["2"]
    _xy(line.stoppingPointOn(forward), 18.0, -1.75)
    _xy(line.stoppingPointOn(backward), 18.0, 1.75)

    legacy = by_id["3"]
    assert legacy.stoppingPointOn(forward) is None
    _xy(legacy.stoppingPointOn(backward), 10.0, 1.75)


def test_stopping_point_on_carla_approach_is_junction(tmp_path):
    """Approach light's halt point is the junction contact, per lane."""
    network = load_network(tmp_path, MAP_APPROACH_SIGNAL)
    light = _signals_by_id(network)["201"]
    approach = next(road for road in network.roads if road.id == 1)
    by_lid = {open_drive_id(lane): lane for lane in approach.lanes}
    _xy(light.stoppingPointOn(by_lid[-1]), 20.0, -1.75)
    _xy(light.stoppingPointOn(by_lid[-2]), 20.0, -5.25)
    _xy(light.position, 18.0, -3.5)


def test_carla_dummy_validity_still_halts_at_near_junction(tmp_path):
    """Town01-style 0-0 validity + opposite orientation still yields a halt."""
    network = load_network(tmp_path, MAP_CARLA_DUMMY_VALIDITY)
    light = _signals_by_id(network)["201"]
    approach = next(road for road in network.roads if road.id == 1)
    by_lid = {open_drive_id(lane): lane for lane in approach.lanes}
    assert light.validity == (0, 0)
    assert light.orientation == "-"
    assert light.stoppingS == 20.0
    assert light.affects(by_lid[-1])
    assert light.affects(by_lid[-2])
    _xy(light.stoppingPointOn(by_lid[-1]), 20.0, -1.75)
    _xy(light.stoppingPointOn(by_lid[-2]), 20.0, -5.25)


def test_traffic_light_picks_nearest_junction_not_orientation():
    """Pole next to s=0 wins over orientation=+ pointing at the far junction."""
    from scenic.domains.driving.roads import Signal

    light = Signal(
        uid="signal360",
        openDriveID=360,
        country="OpenDRIVE",
        type="1000001",
        subtype="-1",
        priorities=(),
        s=2.15,
        t=5.0,
        orientation="+",
    )
    assert light.resolveStoppingS({}, plus_contact=157.5, minus_contact=0.0) == 0.0


def test_halt_point_ahead_picks_nearest_on_lane(tmp_path):
    """haltPointAhead is the next stop along the lane, not behind the ego."""
    from scenic.core.vectors import Vector

    network = load_network(tmp_path, MAP_SIGNAL_PLACEMENT)
    road = network.roads[0]
    forward = next(lane for lane in road.lanes if open_drive_id(lane) == -1)
    ahead = forward.haltPointAhead(Vector(1, -1.75))
    _xy(ahead, 18.0, -1.75)
    assert forward.haltPointAhead(Vector(19, -1.75)) is None
