function login_validation() {
  var uname = document.log.txtuname.value;
  var pwd = document.log.txtpassword.value;

  var valid = true;
  if (uname == null || uname == "") {
    alert("Please enter your user name!");
    uname.focus();
    return (valid = false);
  }
  if (pwd == null || pwd == "") {
    alert("Please enter your password!");
    pwd.focus();
    return (valid = false);
  }
  return valid;
}
