import { Dropdown, Image } from "react-bootstrap";
import profileImg from "../test/profile.jpg"; // adjust path as needed

function logout() {
    localStorage.setItem("access_token", "");
    localStorage.setItem("refresh_token", "");
    window.location.href = "http://localhost:3000/login"
}

function ProfileDropdown() {
  return (
    <Dropdown align="end" className="h-full">
      <Dropdown.Toggle
        variant="light"
        id="dropdown-basic"
        className="h-full border-0 bg-transparent p-0"
      >
        <Image
          src={profileImg.src} // use the imported image URL
          roundedCircle
          alt="Profile"
          className="aspect-square object-cover h-full"
        />
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Item href="#/profile">Profile</Dropdown.Item>
        <Dropdown.Item href="#/settings">Settings</Dropdown.Item>
        <Dropdown.Divider />
        <Dropdown.Item onClick={logout}>Logout</Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
}

export default ProfileDropdown;
